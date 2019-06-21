from rest_framework import serializers

from .models import Schedule, Holiday


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ('participants', )


class ScheduleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('name', 'date', )