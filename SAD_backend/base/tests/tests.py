from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from account.models import Member
from base.models import Library, ContentType, Content


class ContentModelTests(TestCase):

    def setUp(self, er=None) -> None:
        self.member = Member.objects.create(email='m@s.com', password='1234')
        self.library = Library.objects.create(name='l1')
        self.content_type = ContentType.objects.create(name='text')

    def test_content_creation(self):
        self.assertEqual('test', 'test')

