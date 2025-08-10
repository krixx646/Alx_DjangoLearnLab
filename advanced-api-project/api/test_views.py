# /api/test_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPIStep1Tests(TestCase):
    def setUp(self):
        # Users
        self.admin_user = User.objects.create_user(
            username="adminuser", password="adminpass", is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="normaluser", password="normalpass", is_staff=False
        )

        # Authors (assuming Author has a 'name' field)
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Books
        # Make titles and years distinct for filtering/search/ordering tests
        self.book1 = Book.objects.create(
            title="Alpha Book", author=self.author1, publication_year=2000
        )
        self.book2 = Book.objects.create(
            title="Beta Book", author=self.author2, publication_year=2010
        )
        self.book3 = Book.objects.create(
            title="Gamma Book", author=self.author1, publication_year=2005
        )

        # Client
        self.client = APIClient()

        # URL helpers (names must match your urls.py names)
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.update_url = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.delete_url = lambda pk: reverse("book-delete", kwargs={"pk": pk})

    # ---------- List / Read behaviors ----------
    def test_list_books_anonymous_allowed(self):
        """Anyone should be able to GET the book list (AllowAny on list)."""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Expect three books created in setUp
        self.assertEqual(len(resp.data), 3)

    # ---------- Filtering ----------
    def test_filter_books_by_title(self):
        """Filtering by exact title should return matching book(s)."""
        resp = self.client.get(self.list_url, {"title": "Alpha Book"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "Alpha Book")

    # ---------- Searching ----------
    def test_search_books_by_author_name(self):
        """Search should match author name via 'search' param (author__name)."""
        resp = self.client.get(self.list_url, {"search": "Author One"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # author1 has book1 and book3 -> expect 2 results
        self.assertEqual(len(resp.data), 2)
        returned_titles = {b["title"] for b in resp.data}
        self.assertTrue({"Alpha Book", "Gamma Book"}.issubset(returned_titles))

    # ---------- Ordering ----------
    def test_order_books_by_publication_year_desc(self):
        """Ordering by -publication_year should return newest first."""
        resp = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ---------- Create (admin only) ----------
    def test_create_book_as_admin(self):
        """Admin user can create a book (IsAdminUser restriction)."""
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "title": "Delta Book",
            "author": self.author2.pk,  # send author id
            "publication_year": 2022,
        }
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Delta Book").exists())
        self.client.force_authenticate(user=None)

    def test_create_book_as_normal_user_forbidden(self):
        """Non-admin users should be forbidden to create (403)."""
        self.client.force_authenticate(user=self.normal_user)
        payload = {
            "title": "Epsilon Book",
            "author": self.author1.pk,
            "publication_year": 2022,
        }
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))
        self.assertFalse(Book.objects.filter(title="Epsilon Book").exists())
        self.client.force_authenticate(user=None)

    def test_create_book_unauthenticated_forbidden(self):
        """Anonymous requests must not be allowed to create (403)."""
        payload = {
            "title": "Zeta Book",
            "author": self.author1.pk,
            "publication_year": 2022,
        }
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))
        self.assertFalse(Book.objects.filter(title="Zeta Book").exists())

    # ---------- Update (admin only) ----------
    def test_update_book_as_admin(self):
        """Admin can patch (partial update) a book."""
        self.client.force_authenticate(user=self.admin_user)
        resp = self.client.patch(self.update_url(self.book1.pk), {"title": "Alpha Updated"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha Updated")
        self.client.force_authenticate(user=None)

    def test_update_book_as_normal_user_forbidden(self):
        """Non-admin cannot update book."""
        self.client.force_authenticate(user=self.normal_user)
        resp = self.client.patch(self.update_url(self.book2.pk), {"title": "Should Not"}, format="json")
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))
        self.client.force_authenticate(user=None)

    # ---------- Delete (admin only) ----------
    def test_delete_book_as_admin(self):
        """Admin can delete a book."""
        self.client.force_authenticate(user=self.admin_user)
        resp = self.client.delete(self.delete_url(self.book3.pk))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book3.pk).exists())
        self.client.force_authenticate(user=None)

    def test_delete_book_as_normal_user_forbidden(self):
        """Non-admin cannot delete a book."""
        self.client.force_authenticate(user=self.normal_user)
        resp = self.client.delete(self.delete_url(self.book1.pk))
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))
        # ensure still exists
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())
        self.client.force_authenticate(user=None)
