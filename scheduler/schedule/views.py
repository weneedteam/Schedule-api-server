from django.shortcuts import render

from .serializers import ScheduleSerializer

from rest_framework import viewsets, mixins


class ScheduleViewSet(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    serializer_class = ScheduleSerializer