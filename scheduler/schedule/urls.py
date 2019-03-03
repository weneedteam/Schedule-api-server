from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ScheduleViewSet


router = DefaultRouter()
router.register('schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [

]

urlpatterns += router.urls