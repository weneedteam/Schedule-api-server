from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimestampedModel

User = get_user_model()


class FriendRequest(TimestampedModel):
    request_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='request_user',
        verbose_name='요청자',
    )
    response_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='response_user',
        verbose_name='수락자',
    )
    assent = models.BooleanField(
        verbose_name='수락여부'
    )
    assented_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='수락일시',
    )

    def __str__(self):
        return "{} -> {}" .format(self.request_user, self.response_user)

    class Meta:
        db_table = 'friendRequest'
        verbose_name = '친구 요청 상태'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')

    @classmethod
    def get_friend_request_list(cls, **kwargs):
        kwargs.pop('assent', None)
        user_columns = ['id', 'username', 'nickname']
        args = []
        if 'request_user' in kwargs:
            for c in user_columns:
                args.append("request_user__%s" % c)

        if 'response_user' in kwargs:
            for c in user_columns:
                args.append("response_user__%s" % c)

        return cls.objects.filter(assent=False, **kwargs).values(*args)
