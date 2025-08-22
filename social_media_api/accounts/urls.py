from django.urls import path, include
from .views import UserRegistrationView, LoginApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserRegistrationView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginApiView.as_view(), name='login'),
]