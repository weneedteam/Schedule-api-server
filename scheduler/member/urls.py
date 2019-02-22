from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet


router = DefaultRouter()
router.register('user', UserProfileViewSet)

urlpatterns = [

]

urlpatterns += router.urls