from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Device(models.Model):
    ANDROID = 'ANDROID'
    WEB = 'WEB'
    IOS = 'IOS'

    DEVICE_CHOICES = (
        (ANDROID, 'Android'),
        (WEB, 'Web'),
        (IOS, 'Ios'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=400)
    active = models.BooleanField(default=True)
    device_type = models.CharField(max_length=7, choices=DEVICE_CHOICES)
