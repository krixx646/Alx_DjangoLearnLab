# relationship_app/views.py

from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    # Renders the template at relationship_app/list_books.html
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: detail of a library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
