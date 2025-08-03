from django.shortcuts import render
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser #import specific authentication we want to alter

# 📌 Public view — no authentication required
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
   
# 📌 Admin-only full CRUD view
class BookViewSet (viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

# Create your views here.
"""
🔐 API Authentication and Permission Setup:

- All views default to TokenAuthentication (set in settings.py).
- All views require authentication unless explicitly opened (e.g., AllowAny).
- A token can be retrieved by sending a POST request to /api/token/ with valid credentials.
- View permissions are defined per view:
    - BookList: public
    - BookViewSet: admin-only
"""

