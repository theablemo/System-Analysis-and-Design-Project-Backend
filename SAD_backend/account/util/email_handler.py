from account.util.redis_connection import connection
from django.core.mail import send_mail
from backend import settings
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


def send_change_password_email(email, new_password):
    send_mail(
        'password change',
        f'the password is changed and new password is {new_password}',
        settings.EMAIL_HOST_USER,
        [email]
    )


def send_reset_password_email(email, new_password):
    send_mail(
        'password reset',
        f'the password is changed and new password is {new_password}',
        settings.EMAIL_HOST_USER,
        [email]
    )
