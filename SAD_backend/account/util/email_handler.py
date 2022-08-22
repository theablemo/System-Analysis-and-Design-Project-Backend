from account.util.redis_connection import connection
from backend import settings
import random

from backend.tasks import send_email_task


def send_register_email(email):
    code = random.randint(100000, 999999)
    connection.set(email, code, 900)
    send_email_task('registration code', f'the verification code is {code} and is valid for 15 mins',
                    settings.EMAIL_HOST_USER, [email])


def send_change_password_email(email, new_password):
    send_email_task('password change', f'the password is changed and new password is {new_password}',
                    settings.EMAIL_HOST_USER, [email])


def send_reset_password_email(email, new_password):
    send_email_task('password reset', f'the password is changed and new password is {new_password}',
                    settings.EMAIL_HOST_USER, [email])
