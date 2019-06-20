from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()

class Schedule(models.Model):
    registrant = models.ForeignKey(User, on_delete=models.PROTECT, related_name='schedule_registrant')
    participants = models.ManyToManyField(User, related_name='schedule_participants')
    arrival_member = models.ManyToManyField(User, related_name='schedule_arrival_member')
    title = models.CharField(max_length=300)
    state = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    content = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.title


class Holiday(models.Model):
    name = models.CharField(max_length=50)
    is_holiday = models.BooleanField()
    date = models.DateField()

    def __str__(self):
        return "{} [{}]".format(self.name, self.date)