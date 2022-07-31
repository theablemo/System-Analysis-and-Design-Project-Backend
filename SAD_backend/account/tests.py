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

    def check_method(self, response):
        self.check_error(response,
                         status_code=405,
                         message='MethodNotAllowed', )


class AuthorizationTest(ApiV2BaseTests):

    def register_user(self, username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei',gender=1):
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
        r = self.register_user(username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei', gender=1)
        self.assertEqual(r.status_code, 200)
        r = json.loads(r.content)

        self.assertEqual(r['code'], 'OK')
        self.assertIn('token', r)
        self.assertIn('token', r['token'])
        self.assertIn('refreshToken', r['token'])
        self.assertIn('validUntil', r['token'])
        member = self.get_member_with_username('amir@gmail.com')
        self.assertIsNotNone(member)
        self.assertEqual(member.first_name, 'amirreza')
        self.assertEqual(member.last_name, 'mirzaei')
        self.assertFalse(member.is_superuser)
        self.assertTrue(member.check_password('12345'))
        self.assertEqual(member.gender, 1)

    def test_register_bad_gender(self):
        r = self.register_user(username='amir@gmail.com', password='12345', firstName='amirreza', lastName='mirzaei', gender=19)
        self.check_error(r)
        r = json.loads(r.content)
        self.assertNotIn('token', r)
