from rest_framework import serializers

from .models import Schedule, Holiday


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ('participants', 'arrival_member')


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('name', 'date', )
