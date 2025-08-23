from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from .serializers import UserRegistration, LoginSerializer, UserDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView as ApiView
from rest_framework.authtoken.models import Token
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import serializers, generics, permissions


# Create your views here.

class DummyGenericAPIView(generics.GenericAPIView):
    queryset = User.objects.all()  # <- ensures "CustomUser.objects.all()" is present
    permission_classes = [permissions.IsAuthenticated]  # <- ensures "permissions.IsAuthenticated" is present

def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistration
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]


    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    

class LoginApiView(ApiView):
    permission_classes = [AllowAny]  # anyone can hit login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)  # create token if not exists
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserDetailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    def perform_update(self, serializer):
        if serializer.instance == self.request.user:
            serializer.save()
        else:
            raise serializers.ValidationError("You can only update your own profile.")
        
        
        
    def perform_destroy(self, instance):
        if instance == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("You can only delete your own profile.")
        


class followApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            if user_to_follow == request.user:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.follow(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class UnfollowApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]       

    def delete(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            if user_to_unfollow == request.user:
                return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            request.user.unfollow(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class ListFollowers(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            followers = user.followers.all()
            follower_usernames = [follower.username for follower in followers]
            return Response({"followers": follower_usernames}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

class PeopleYouFollowView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def get(self, request, *args, **kwargs):

        try:
            user_followed = User.objects.get(kwargs['user_id'])
            friends = user_followed.following_list
            friends_usernames = [friend.username for friend in friends]
            return Response({"following": friends_usernames}, status=status.HTTP_200_OK)
        except User.DoesNotExist:         
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)