# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # site & posts (using names your templates expect)
    path('', views.PostListView.as_view(), name='home'),           # Home -> posts list
    path('post/', views.PostListView.as_view(), name='posts'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # auth/profile (these should match the names used in your base.html)
    path('register/', views.signup_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    path('posts/<int:post_pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_pk>/comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('posts/<int:post_pk>/comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
