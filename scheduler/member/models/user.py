from django.db import models
from django.contrib.auth.models import AbstractUser

from member.models.user_manager import UserManager
from utils.models import TimestampedModel


class User(AbstractUser):
    username = None
    nickname = None
    email = models.EmailField(
        unique=True,
        verbose_name='이메일',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'User(ID {self.id})'

    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')


class UserProfile(TimestampedModel):
    KOREAN = 'KR'
    ENGLISH = 'EN'

    LANGUAGE_CHOICES = (
        (KOREAN, 'Korean'),
        (ENGLISH, 'English'),
    )

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='유저',
    )
    username = models.CharField(
        max_length=30,
        verbose_name='이름',
    )
    nickname = models.CharField(
        max_length=30,
        verbose_name='닉네임',
    )
    birth = models.DateField(
        verbose_name='생년월일',
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="KR",
        verbose_name='언어',
    )
    friends = models.ManyToManyField(
        to=User,
        related_name='friends',
        verbose_name='친구목록',
    )

    def __str__(self):
        return f'UserProfile(ID {self.id}, by {self.user}, at {self.datetime})'

    class Meta:
        db_table = 'userProfile'
        verbose_name = '프로필'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')

    def get_friends(self, *args, **kwargs):
        return self.friends.filter(**kwargs).values('id', 'username', 'nickname', *args)
