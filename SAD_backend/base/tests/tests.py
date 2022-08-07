import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from account.models import Member
from backend.settings import CONTENTS_DIR
from base.models import Library, ContentType, Content


class ContentModelTests(TestCase):

    def setUp(self, er=None) -> None:
        self.member = Member(email='m@s.com')
        self.member.set_password('1234')
        self.member.save()
        self.library = Library.objects.create(name='l1')
        self.content_type = ContentType.objects.create(name='text')
        self.filename = 'test.txt'
        self.file = SimpleUploadedFile(self.filename, b'Sample Content.')

    def test_content_creation(self):
        Content.objects.create(
            filename=self.filename,
            member=self.member,
            type=self.content_type,
            file=self.file,
            library=self.library
        )
        content_count = Content.objects.filter(filename=self.filename).count()
        self.assertEqual(content_count, 1)
        content = Content.objects.get(filename=self.filename)
        self.assertEqual(content.library.name, self.library.name)
        self.assertEqual(content.path, f'{CONTENTS_DIR}{self.member.id}_{self.library.name}_'
                                       f'{self.filename.split(".")[0]}_{self.filename}')

    def tearDown(self):
        path = CONTENTS_DIR
        for file_name in os.listdir(path):
            file = path + file_name
            os.remove(file)


class ContentViewTest(TestCase):
    def setUp(self, er=None) -> None:
        self.library = Library.objects.create(name='l1')
        self.content_type = ContentType.objects.create(name='text')
        self.filename = 'test.txt'
        self.file = SimpleUploadedFile(self.filename, b'Sample Content.')
        self.member = Member(username='m@s.com')
        self.member.set_password('1234')
        self.member.save()
        resp = self.client.post('/api/login', {'username': 'm@s.com', 'password': '1234'}).json()
        self.token = resp['token']['token']

    def test_upload_view(self):
        # TODO: User is not Authenticated
        data = {
            'library': self.library.name,
            'type': self.content_type.name,
            'file': self.file,
        }
        response = self.client.post('/api/content/new/', data=data, HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 200)
        content_count = Content.objects.filter(filename=self.filename).count()
        self.assertEqual(content_count, 1)
