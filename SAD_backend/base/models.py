from django.db import models


# Create your models here.
from account.models import Member
from backend.settings import CONTENTS_DIR


class ContentType(models.Model):
    pass


class AttachmentType(models.Model):
    pass


class Library(models.Model):
    pass


class Content(models.Model):
    name = models.CharField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date_created = models.DateField(verbose_name='date_created')
    type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    @property
    def path(self):
        return f'{CONTENTS_DIR}{self.member.id}/{self.name}'


class Attachment(models.Model):
    pass
