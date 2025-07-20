# relationship_app/urls.py

from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import register
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('books/', list_books),
    path('libraries/<int:pk>/', LibraryDetailView.as_view()),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
