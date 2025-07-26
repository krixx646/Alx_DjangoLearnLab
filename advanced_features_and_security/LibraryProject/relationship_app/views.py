# relationship_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Library, UserProfile

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

def edit_book_redirect(request):
    # Redirect to a default book edit page or raise an error
    return redirect('list_books')  # or HttpResponseNotFound or similar

# Class-based view: detail of a library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

# Function-based view: user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# --- Role-based Views ---

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# --- Permission-Protected Book Actions ---

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    # Placeholder logic
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    # Placeholder logic
    return render(request, 'relationship_app/edit_book.html')

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    # Placeholder logic
    return render(request, 'relationship_app/delete_book.html')
