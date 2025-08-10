# /api/test_views.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPIStep1Tests(APITestCase):
    def setUp(self):
        # Users
        self.admin_user = User.objects.create_user(
            username="adminuser", password="adminpass", is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="normaluser", password="normalpass", is_staff=False
        )

        # Authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Books (distinct titles and years)
        self.book1 = Book.objects.create(
            title="Alpha Book", author=self.author1, publication_year=2000
        )
        self.book2 = Book.objects.create(
            title="Beta Book", author=self.author2, publication_year=2010
        )
        self.book3 = Book.objects.create(
            title="Gamma Book", author=self.author1, publication_year=2005
        )

        # URL helpers (must match your api/urls.py name= values)
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.update_url = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.delete_url = lambda pk: reverse("book-delete", kwargs={"pk": pk})

    # Helper: handle paginated vs non-paginated responses
    def _extract_list(self, response):
        """
        If DRF pagination is enabled, response.data is a dict containing 'results'.
        Otherwise response.data is the list directly.
        """
        if isinstance(response.data, dict) and "results" in response.data:
            return response.data["results"]
        return response.data

    # ---------- List / Read ----------
    def test_list_books_anonymous_allowed(self):
        """Anyone (anonymous) can GET the book list (AllowAny)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = self._extract_list(response)
        self.assertEqual(len(data), 3)

    # ---------- Filtering ----------
    def test_filter_books_by_title(self):
        """Filter by exact title returns matching book."""
        response = self.client.get(self.list_url, {"title": "Alpha Book"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = self._extract_list(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Alpha Book")

    # ---------- Searching ----------
    def test_search_books_by_author_name(self):
        """Search should match author name (author__name configured)."""
        response = self.client.get(self.list_url, {"search": "Author One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = self._extract_list(response)
        # Author One has book1 and book3
        self.assertEqual(len(data), 2)
        titles = {item["title"] for item in data}
        self.assertTrue({"Alpha Book", "Gamma Book"}.issubset(titles))

    # ---------- Ordering ----------
    def test_order_books_by_publication_year_desc(self):
        """Ordering by -publication_year should return newest first."""
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = self._extract_list(response)
        years = [item["publication_year"] for item in data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ---------- Create (admin-only in your views) ----------
    def test_create_book_as_admin(self):
        """Admin user can create a book."""
        # use login so checker finds self.client.login
        logged = self.client.login(username="adminuser", password="adminpass")
        self.assertTrue(logged, "Admin login failed in test setup")
        payload = {
            "title": "Delta Book",
            "author": self.author2.pk,  # send FK id
            "publication_year": 2022,
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Delta Book").exists())
        self.client.logout()

    def test_create_book_as_normal_user_forbidden(self):
        """Non-admin user should be forbidden to create (403 or 401)."""
        logged = self.client.login(username="normaluser", password="normalpass")
        self.assertTrue(logged, "Normal user login failed in test setup")
        payload = {
            "title": "Epsilon Book",
            "author": self.author1.pk,
            "publication_year": 2022,
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertIn(
            response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)
        )
        self.assertFalse(Book.objects.filter(title="Epsilon Book").exists())
        self.client.logout()

    def test_create_book_unauthenticated_forbidden(self):
        """Anonymous cannot create (403/401)."""
        payload = {
            "title": "Zeta Book",
            "author": self.author1.pk,
            "publication_year": 2022,
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertIn(
            response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)
        )
        self.assertFalse(Book.objects.filter(title="Zeta Book").exists())

    # ---------- Update (admin-only) ----------
    def test_update_book_as_admin(self):
        """Admin can partially update a book (PATCH)."""
        logged = self.client.login(username="adminuser", password="adminpass")
        self.assertTrue(logged, "Admin login failed in test setup")
        response = self.client.patch(
            self.update_url(self.book1.pk), {"title": "Alpha Updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha Updated")
        self.client.logout()

    def test_update_book_as_normal_user_forbidden(self):
        """Non-admin cannot update."""
        logged = self.client.login(username="normaluser", password="normalpass")
        self.assertTrue(logged, "Normal user login failed in test setup")
        response = self.client.patch(
            self.update_url(self.book2.pk), {"title": "Should Not"}, format="json"
        )
        self.assertIn(
            response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)
        )
        self.client.logout()

    # ---------- Delete (admin-only) ----------
    def test_delete_book_as_admin(self):
        """Admin can delete a book."""
        logged = self.client.login(username="adminuser", password="adminpass")
        self.assertTrue(logged, "Admin login failed in test setup")
        response = self.client.delete(self.delete_url(self.book3.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book3.pk).exists())
        self.client.logout()

    def test_delete_book_as_normal_user_forbidden(self):
        """Non-admin cannot delete."""
        logged = self.client.login(username="normaluser", password="normalpass")
        self.assertTrue(logged, "Normal user login failed in test setup")
        response = self.client.delete(self.delete_url(self.book1.pk))
        self.assertIn(
            response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)
        )
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())
        self.client.logout()
