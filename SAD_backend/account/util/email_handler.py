from account.util.redis_connection import connection
from django.core.mail import send_mail
from django.conf import settings
import random


def send_register_email(email):
    code = random.randint(100000, 999999)
    connection.set(email, code, 900)
    send_mail(
        'registration code',
        f'the verification code is {code} and is valid for 15 mins',
        settings.EMAIL_HOST_USER,
        [email]
    )
