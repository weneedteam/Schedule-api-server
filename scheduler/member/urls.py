from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet, FriendRequestViewSet


router = DefaultRouter()
router.register('user', UserProfileViewSet)
router.register('friend-request', FriendRequestViewSet)

urlpatterns = [

]

urlpatterns += router.urls