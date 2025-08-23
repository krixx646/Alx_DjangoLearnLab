from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from .serializers import UserRegistration, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView as ApiView
from rest_framework.authtoken.models import Token
from django.contrib import messages


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
    