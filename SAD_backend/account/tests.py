import json
from django.test import TestCase
from account.models import Member


class ApiV2BaseTests(TestCase):
    do_login = False

    def setUp(self):
        super(ApiV2BaseTests, self).setUp()

    def check_success(self, response):
        self.assertEqual(response.status_code, 200)

    def check_error(self, response, status_code=400, code=None, message=None, description=None):
        self.assertEqual(response.status_code, status_code)
        r = json.loads(response.content)
        if code:
            self.assertEqual(r['code'], code)
        if message:
            self.assertEqual(r['message'], message)
        if description:
            self.assertEqual(r['description'], description)

    def check_authorization(self, response):
        self.check_error(response,
                         status_code=401,
                         message='NoToken', )


class AuthorizationTest(ApiV2BaseTests):

    def register_user(self, username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei',
                      gender=1):
        r = self.client.post('/api/register', {
            'username': username,
            'password': password,
            'first_name': firstName,
            'last_name': lastName,
            'gender': gender,
        })
        return r

    def get_member_with_username(self, username):
        return Member.objects.filter(username=username).first()

    def test_register_successful(self):
        r = self.register_user(username='amirreza2001@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei',
                               gender=1)
        self.assertEqual(r.status_code, 200)
        r = json.loads(r.content)

        self.assertEqual(r['code'], 'OK')
        member = self.get_member_with_username('amirreza2001@gmail.com')
        self.assertIsNotNone(member)
        self.assertEqual(member.first_name, 'amirreza')
        self.assertEqual(member.last_name, 'mirzaei')
        self.assertFalse(member.is_superuser)
        self.assertTrue(member.check_password('12345'))
        self.assertEqual(member.gender, 1)

    def test_register_bad_gender(self):
        r = self.register_user(username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei',
                               gender=19)
        self.check_error(r)
        r = json.loads(r.content)
        member = self.get_member_with_username('amir@gmail.com')
        self.assertIsNone(member)

    def test_register_no_name(self):
        r = self.client.post('/api/register', {
            'username': 'amirreza@gmail.com',
            'password': '12345',
            'last_name': 'mirzaei',
            'gender': 1,
        })
        member = self.get_member_with_username('amirreza@gmail.com')
        self.assertIsNone(member)

    def test_login_ok(self):
        r = self.register_user(username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei',
                               gender=1)
        r = self.client.post('/api/login', {
            'username': 'amir@gmail.com',
            'password': '12345'
        })
        self.check_success(r)
        r = json.loads(r.content)

        self.assertIn('token', r)
        token = r['token']
        self.assertEqual(len(token['token']), 205)
        self.assertEqual(len(token['refreshToken']), 207)
        self.assertNotEqual(token['token'], token['refreshToken'])

    def test_login_no_such_user(self):
        r = self.client.post('/api/login', {
            'username': 'amir@gmail.com',
            'password': '12345'
        })

        self.check_error(r)
        r = json.loads(r.content)
        self.assertNotIn('token', r)


    def test_login_invalid_password(self):
        r = self.register_user(username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei',
                               gender=1)

        r = self.client.post('/api/login', {
            'username': 'amir@gmail.com',
            'password': '123452132413'
        })

        self.check_error(r)
        r = json.loads(r.content)
        self.assertNotIn('token', r)

    def test_check_username_not_allowed_method(self):
        r = self.client.get('/api/check-username', {
            'username': '',
        })
        self.check_error(r, status_code=405)

    def test_check_username_exists(self):
        r = self.register_user(username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei',
                               gender=1)
        r = self.client.post('/api/check-username', {
            'username': 'amir@gmail.com',
        })

        self.check_success(r)
        r = json.loads(r.content)
        self.assertEquals(r['exist'], True)

    def test_check_username_not_exists(self):
        r = self.client.post('/api/check-username', {
            'username': 'amir@gmail.com',
        })

        self.check_success(r)
        r = json.loads(r.content)
        self.assertEquals(r['exist'], False)
