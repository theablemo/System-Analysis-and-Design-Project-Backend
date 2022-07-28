from django.db import models

# Create your models here.
from account.models import Member
from base.utils.file_utils import content_file_path, attachment_file_path


class ContentType(models.Model):
    name = models.CharField()

    @classmethod
    def get_default_type_pk(cls):
        obj, _ = cls.objects.get_or_create(name='other')
        return obj.pk


class AttachmentType(models.Model):
    name = models.CharField()

    @classmethod
    def get_default_type_pk(cls):
        obj, _ = cls.objects.get_or_create(name='other')
        return obj.pk


class Library(models.Model):
    name = models.CharField()
    type = models.ForeignKey(ContentType,
                             default=ContentType.get_default_type_pk,
                             on_delete=models.SET_DEFAULT)
    date_created = models.DateTimeField(verbose_name='date_created')


class Content(models.Model):
    filename = models.CharField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name='date_created')
    type = models.ForeignKey(ContentType,
                             default=ContentType.get_default_type_pk,
                             on_delete=models.SET_DEFAULT)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    file = models.FileField(upload_to=content_file_path)

    @property
    def path(self):
        return content_file_path(self, self.filename)


class Attachment(models.Model):
    filename = models.CharField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    type = models.ForeignKey(AttachmentType,
                             default=AttachmentType.get_default_type_pk,
                             on_delete=models.SET_DEFAULT)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file = models.FileField(upload_to=attachment_file_path)

    @property
    def path(self):
        return attachment_file_path(self, self.filename)
