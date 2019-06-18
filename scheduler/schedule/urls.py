from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ScheduleViewSet, HolidayViewSet


router = DefaultRouter()
router.register('schedule', ScheduleViewSet, basename='schedule')
router.register('holiday', HolidayViewSet)

urlpatterns = [

]

urlpatterns += router.urls