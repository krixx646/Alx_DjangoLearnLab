# relationship_app/views.py
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    lines = [f"{book.title} by {book.author.name}" for book in books]
    return HttpResponse("\n".join(lines))

# Class-based view: detail of a library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'