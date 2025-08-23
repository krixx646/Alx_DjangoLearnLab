from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import serializers
# Create your views here.

# notifications/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    def perform_destroy(self, instance):
        if instance.recipient == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("You can only delete your own notifications.")