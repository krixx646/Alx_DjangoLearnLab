from django.urls import path
from .views import AuthorCreateView, AuthorListView, AuthorDetailView, AuthorUpdateView, AuthorDeleteView, BookCreateView, BookListView, BookDetailView, BookUpdateView, BookDeleteView

urlpatterns = [
     # Author URLs
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', AuthorCreateView.as_view(), name='author-create'),
    path('authors/update/', AuthorUpdateView.as_view(), name='author-update'),
    path('authors/delete/', AuthorDeleteView.as_view(), name='author-delete'),
    # Book URLs
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),

]