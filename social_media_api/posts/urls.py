from django.urls import path, include
from .views import PostViewSet, CommentViewSet, LikeViewSet, EmojiViewSet, FeedView
from . import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'emojis', EmojiViewSet, basename='emoji')


urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', views.PostLikeView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', views.PostUnlikeView.as_view(), name='post-unlike'),
]