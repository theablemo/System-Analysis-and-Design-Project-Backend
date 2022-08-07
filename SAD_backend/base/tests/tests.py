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

    def test_upload_view_successful(self):
        data = {
            'library': self.library.name,
            'type': self.content_type.name,
            'file': self.file,
        }
        response = self.client.post('/api/content/new/', data=data, HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 200)
        content_count = Content.objects.filter(filename=self.filename).count()
        self.assertEqual(content_count, 1)

    def test_upload_view_duplicate_content(self):
        Content.objects.create(
            member=self.member,
            library=self.library,
            type=self.content_type,
            file=self.file,
            filename=self.filename
        )
        data = {
            'library': self.library.name,
            'type': self.content_type.name,
            'file': SimpleUploadedFile(self.filename, b'Sample Content.'),
        }
        response = self.client.post('/api/content/new/', data=data, HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'][0], 'Content already exists.')

    def test_download_view_successful(self):
        Content.objects.create(
            member=self.member,
            library=self.library,
            type=self.content_type,
            file=self.file,
            filename=self.filename
        )
        response = self.client.get(f'/api/download/{self.library.name}/{self.filename}/', HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)
        self.assertEqual(response.headers['Content-Type'], 'text/plain')

    def test_download_view_content_not_found(self):
        Content.objects.all().delete()
        response = self.client.get(f'/api/download/{self.library.name}/{self.filename}/', HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Content.objects.all().delete()
        path = CONTENTS_DIR
        for file_name in os.listdir(path):
            file = path + file_name
            os.remove(file)


class ContentListViewTest(TestCase):
    def setUp(self) -> None:
        self.library = Library.objects.create(name='l1')
        self.content_type = ContentType.objects.create(name='text')
        self.member = Member(username='m@s.com')
        self.member.set_password('1234')
        self.member.save()
        resp = self.client.post('/api/login', {'username': 'm@s.com', 'password': '1234'}).json()
        self.token = resp['token']['token']

        self.filename1 = 'test1.txt'
        self.file1 = SimpleUploadedFile(self.filename1, b'Sample Content1.')
        self.filename2 = 'test2.txt'
        self.file2 = SimpleUploadedFile(self.filename2, b'Sample Content2.')
        self.filename3 = 'test3.txt'
        self.file3 = SimpleUploadedFile(self.filename3, b'Sample Content3.')
        Content.objects.bulk_create([
            Content(member=self.member, library=self.library, file=self.file1,
                    filename=self.filename1, type=self.content_type),
            Content(member=self.member, library=self.library, file=self.file2,
                    filename=self.filename2, type=self.content_type),
            Content(member=self.member, library=self.library, file=self.file3,
                    filename=self.filename3, type=self.content_type), ]

        )

    def test_get_all_contents(self):
        response = self.client.get('/api/content/all/', HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        for item in response.json():
            self.assertEqual(self.member.id, int(item.get('member_id')))
            self.assertEqual(self.library.name, item.get('library'))

    def tearDown(self):
        Content.objects.all().delete()
        path = CONTENTS_DIR
        for file_name in os.listdir(path):
            file = path + file_name
            os.remove(file)
