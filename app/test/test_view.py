from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from mixer.backend.django import mixer
from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.hashers import make_password, check_password
import json
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User, AnonymousUser
from app.models import User, CustomUserManager
from app import token

from app.views import AccountViewset


class TestAppView(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup = reverse('user-signup')
        self.login = reverse('user-login')
        self.listaccount = reverse('user-listaccounts')
        self.user = mixer.blend('app.User', phonenumber='09111234567', password='1234', is_active=True)
        self.user.password = make_password(self.user.password)
        self.user.save(update_fields=["password"])

    def test_view_signup(self):
        response = self.client.post(self.signup,
                                    {'phonenumber': '09131949275', 'password': 'far@13720216', 'is_shop_owner': True,
                                     'gender': 'female', 'username': 'farinaz'})
        self.assertEquals(response.status_code, 201)

    def test_view_signup_duplicated_phonenumber(self):
        response = self.client.post(self.signup,
                                    {'phonenumber': '09111234567', 'password': 'far@13720216', 'is_shop_owner': True,
                                     'gender': 'female', 'username': 'farinaz'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json()['data']['phonenumber'], ['user with this phonenumber already exists.'])

    def test_view_signup_miss_required_field(self):
        response = self.client.post(self.signup,
                                    {'phonenumber': '09131051401', 'password': 'far@13720216', 'is_shop_owner': True,
                                     'username': 'farinaz'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json()['data']['gender'], ['This field is required.'])

    def test_view_signup_wrong_phonenumber(self):
        response = self.client.post(self.signup,
                                    {'phonenumber': '0913105140', 'password': 'far@13720216', 'is_shop_owner': True,
                                     'username': 'farinaz'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json()['data']['phonenumber'],
                          ['Only digit  and 11 characters with 0 at first of that.'])

    def test_view_login(self):
        response = self.client.post(self.login, {'phonenumber': '09111234567', 'password': '1234'})
        self.assertEquals(response.status_code, 200)

    def test_view_login_invalid_fields(self):
        response = self.client.post(self.login, {'phonenumber': '0911123456', 'password': '1234'})
        self.assertEquals(response.json()['message'], 'Invalid Phonenumber or Password')
        self.assertEquals(response.status_code, 401)

    def test_view_login_bad_request(self):
        response = self.client.post(self.login, {'phonenumber': '0911123456'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json()['message'], 'bad request')

    def test_view_listaccounts(self):
        get_token = token.get_tokens_for_user(User.objects.get(phonenumber=self.user.phonenumber))
        response = self.client.post(self.login, {'phonenumber': '09111234567', 'password': '1234'})

        if response.status_code == 200:
            response = self.client.get(self.listaccount,
                                       headers={'Authorization': 'Bearer ' + str(get_token['access'])})
            self.assertEquals(response.status_code, 200)

            response = self.client.get(self.listaccount, headers={})
            self.assertEquals(response.status_code, 401)
            self.assertEquals(response.json()['detail'], 'Authentication credentials were not provided.')

            response = self.client.get(self.listaccount,
                                       headers={'Authorization': 'Bearer ' + str(get_token['refresh'])})
            self.assertEquals(response.status_code, 401)
            self.assertEquals(response.json()['detail'], 'Given token not valid for any token type')
        else:
            self.assertEquals(response.status_code, 401)
            self.assertEquals(response.json()['detail'], 'Authentication credentials were not provided.')
