from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Post, Comment, Like, Emoji
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, EmojiSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers
from rest_framework import generics, permissions
from rest_framework.views import APIView
# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author']      # exact filtering
    search_fields = ['title', 'content']        # partial search
    ordering_fields = ['created_at', 'likes']   # fields you can sort by
    ordering = ['-created_at']   

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer = PostSerializer(data=self.request.data)
        if serializer.is_valid() and serializer.validated_data['author'] == self.request.user:
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("You can only update your own posts.")
        
    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("You can only delete your own posts.")



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer = PostSerializer(data=self.request.data)
        if serializer.is_valid() and serializer.validated_data['author'] == self.request.user:
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("You can only update your own comments.")
        
    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("You can only delete your own comments.")
        
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        if Post.author == self.request.user:
            raise serializers.ValidationError("You cannot like your own post dummy!.")
        if Like.objects.filter(post=serializer.validated_data['post'], user=self.request.user).exists():
            raise serializers.ValidationError("You have already liked this post.")
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("You can only delete your own likes.")
        

class EmojiViewSet(viewsets.ModelViewSet):
    queryset = Emoji.objects.all()
    serializer_class = EmojiSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'post', 'user']      # exact filtering
    search_fields = ['name']        # partial search
    ordering_fields = ['created_at']   # fields you can sort by


    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        if Post.author == self.request.user:
            raise serializers.ValidationError("You cannot react to your own post dummy!.")
        if Emoji.objects.filter(post=serializer.validated_data['post'], user=self.request.user, name=serializer.validated_data['name']).exists():
            raise serializers.ValidationError("You cannot react to a certain post twice.")
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("You can only delete your own reactions.")
        

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author']      # exact filtering
    search_fields = ['title', 'content']        # partial search
    ordering_fields = ['created_at', 'likes']   # fields you can sort by
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        # Assuming you have a 'followers' ManyToManyField on your User model
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')  
    

