from datetime import datetime
import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models


class GenderChoice(models.IntegerChoices):
    MALE = 1, 'male'
    FEMALE = 2, 'female'


class Member(AbstractUser):
    username = None
    gender = models.PositiveSmallIntegerField(verbose_name='gender', choices=GenderChoice.choices, null=True)
    last_seen = models.DateTimeField(verbose_name='last_seen', default=datetime.fromtimestamp(0, tz=pytz.UTC))
    email = models.EmailField(verbose_name='email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __repr__(self):
        return f"user#{self.id}"

    def __str__(self):
        return self.email