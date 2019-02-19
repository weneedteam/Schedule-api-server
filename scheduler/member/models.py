from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'nickname', ]


class UserProfile():
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    LANGUAGE_CLASS = (
        ('KR', 'Korean'),
        ('EN', 'English'),
    )

    birth = models.DateField(null=False, blank=False)
    language = models.CharField(max_length=2, choices=LANGUAGE_CLASS, default="KR", null=False, blank=True)