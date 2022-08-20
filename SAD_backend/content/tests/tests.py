import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from account.models import Member
from backend.settings import CONTENTS_DIR
from content.models import Library, ContentType, Content


class ContentModelTests(TestCase):

    def setUp(self, er=None) -> None:
        self.member = Member(email='m@s.com')
        self.member.set_password('1234')
        self.member.save()
        self.library = Library.objects.create(name='l1', type='text', member=self.member)
        self.content_type = ContentType.objects.create(name='text')
        self.filename = 'test.txt'
        self.file = SimpleUploadedFile(self.filename, b'Sample Content.')

    def test_content_creation(self):
        Content.objects.create(
            member=self.member,
            type=self.content_type,
            file=self.file,
            library=self.library
        )
        content_count = Content.objects.all().count()
        self.assertEqual(content_count, 1)
        content = Content.objects.get(id=1)
        self.assertEqual(content.library.name, self.library.name)

    def tearDown(self):
        path = CONTENTS_DIR
        for file_name in os.listdir(path):
            file = path + file_name
            os.remove(file)


class ContentViewTest(TestCase):
    def setUp(self, er=None) -> None:
        self.member = Member(username='m@s.com')
        self.member.set_password('1234')
        self.member.save()
        resp = self.client.post('/api/login', {'username': 'm@s.com', 'password': '1234'}).json()
        self.token = resp['token']['token']

        self.library = Library.objects.create(name='l1', type='text', member=self.member)
        self.content_type = ContentType.objects.create(name='txt', type='text')
        self.filename = 'test.txt'
        self.file = SimpleUploadedFile(self.filename, b'Sample Content.')

    def test_upload_view_successful(self):
        data = {
            'library': self.library.pk,
            'file': self.file,
        }
        response = self.client.post('/api/content/', data=data, HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 200)
        content_count = Content.objects.all().count()
        self.assertEqual(content_count, 1)
        content = Content.objects.all().last()
        self.assertEqual(content.type.name, self.content_type.name)

    def test_upload_view_wrong_library(self):
        another_library = Library.objects.create(name='l2', type='video', member=self.member)
        data = {
            'library': another_library.id,
            'file': self.file,
        }
        response = self.client.post('/api/content/', data=data, HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'][0], 'Content and library must be of the same type.')

    def test_download_view_successful(self):
        content = Content.objects.create(
            member=self.member,
            library=self.library,
            type=self.content_type,
            file=self.file,
        )
        response = self.client.get(f'/api/download/{content.path.split("/")[-1]}', HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)
        self.assertEqual(response.headers['Content-Type'], 'text/plain')

    def test_download_view_content_not_found(self):
        Content.objects.all().delete()
        response = self.client.get(f'/api/download/test.txt/', HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 404)

    def test_add_info_to_content(self):
        content = Content.objects.create(
            member=self.member,
            library=self.library,
            type=self.content_type,
            file=self.file,
        )
        import json
        data = {
            'id': content.id,
            'info': {
                "author": "James",
                "description": "Test"
            }
        }
        response = self.client.put('/api/add-info-to-content/',
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   HTTP_X_TOKEN=self.token)
        self.assertEqual(response.status_code, 200)
        content = Content.objects.get(id=content.id)
        import json
        info = json.loads(content.info)
        self.assertEqual(info['author'], 'James')
        self.assertEqual(info['description'], 'Test')

    def tearDown(self):
        Content.objects.all().delete()
        path = CONTENTS_DIR
        for file_name in os.listdir(path):
            file = path + file_name
            os.remove(file)


class ContentListViewTest(TestCase):
    def setUp(self) -> None:
        self.member = Member(username='m@s.com')
        self.member.set_password('1234')
        self.member.save()
        resp = self.client.post('/api/login', {'username': 'm@s.com', 'password': '1234'}).json()
        self.token = resp['token']['token']

        self.library = Library.objects.create(name='l1', type='text', member=self.member)
        self.content_type = ContentType.objects.create(name='text')

        self.filename1 = 'test1.txt'
        self.file1 = SimpleUploadedFile(self.filename1, b'Sample Content1.')
        self.filename2 = 'test2.txt'
        self.file2 = SimpleUploadedFile(self.filename2, b'Sample Content2.')
        self.filename3 = 'test3.txt'
        self.file3 = SimpleUploadedFile(self.filename3, b'Sample Content3.')
        Content.objects.bulk_create([
            Content(member=self.member, library=self.library, file=self.file1, ),
            Content(member=self.member, library=self.library, file=self.file2, ),
            Content(member=self.member, library=self.library, file=self.file3, ),
        ]
        )

    def tearDown(self):
        Content.objects.all().delete()
        path = CONTENTS_DIR
        for file_name in os.listdir(path):
            file = path + file_name
            os.remove(file)


class LibraryUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.member = Member(username='m@s.com')
        self.member.set_password('1234')
        self.member.save()
        resp = self.client.post('/api/login', {'username': 'm@s.com', 'password': '1234'}).json()
        self.token = resp['token']['token']

        self.library = Library.objects.create(name='l1', type='text', member=self.member)
        self.content_type = ContentType.objects.create(type='text')
        ContentType.objects.create(type='video')

    def test_update_name(self):
        data = {'id': self.library.id, 'name': 'library1'}
        response = self.client.put('/api/library/', data=json.dumps(data), HTTP_X_TOKEN=self.token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        updated = Library.objects.get(id=self.library.id)
        self.assertEqual(updated.name, 'library1')

    def test_update_type_when_lib_is_empty(self):
        data = {'id': self.library.id, 'type': 'video'}
        response = self.client.put('/api/library/', data=json.dumps(data), HTTP_X_TOKEN=self.token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        updated = Library.objects.get(id=self.library.id)
        self.assertEqual(updated.type, 'video')

    def test_update_type_when_lib_is_not_empty(self):
        Content.objects.create(
            member=self.member,
            library=self.library,
            type=self.content_type,
            file=SimpleUploadedFile('test.txt', b'Sample Content.'),
        )
        data = {'id': self.library.id, 'type': 'video'}
        response = self.client.put('/api/library/', data=json.dumps(data), HTTP_X_TOKEN=self.token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['code'], 'ERROR')

    def test_update_lib_not_found(self):
        data = {'id': self.library.id + 1, 'name': 'new_library'}
        response = self.client.put('/api/library/', data=json.dumps(data), HTTP_X_TOKEN=self.token,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Content.objects.all().delete()
        path = CONTENTS_DIR
        for file_name in os.listdir(path):
            file = path + file_name
            os.remove(file)
