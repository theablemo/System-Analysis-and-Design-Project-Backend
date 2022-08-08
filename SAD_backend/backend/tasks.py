from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True, max_retries=2)
def send_email_task(self, subject, message, sender, receiver):
    send_mail(subject, message, sender, receiver)
