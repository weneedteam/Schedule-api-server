from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet, FriendRequestViewSet, user_email_validate, user_nickname_validate


router = DefaultRouter()
router.register('user', UserProfileViewSet)
router.register('friend-request', FriendRequestViewSet)

urlpatterns = [
    path('email-validate/', user_email_validate),
    path('nickname-validate/', user_nickname_validate),
]

urlpatterns += router.urls
