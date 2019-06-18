from rest_framework import serializers

from .models import Schedule, Holiday


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ('participants', )


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('name', 'date', )