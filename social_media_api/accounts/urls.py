from django.urls import path, include
from .views import UserRegistrationView, LoginApiView, UserDetailView, ListFollowers, PeopleYouFollowView, followApiView, UnfollowApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserRegistrationView, basename='user')
router.register(r'user-details', UserDetailView, basename='user-detail')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginApiView.as_view(), name='login'),
    path('register/', include),
    path('followers/', ListFollowers.as_view(), name='followers'),
    path('follow/<int:user_id>', followApiView.as_view(), name='follow'),
    path('unfollow/<int:user_id>', UnfollowApiView.as_view(), name='unfollow'),
    path('following/<int:user_id>', PeopleYouFollowView.as_view(), name='following')
]