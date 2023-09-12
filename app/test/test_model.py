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


class TestAppModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup = reverse('user-signup')
        self.login = reverse('user-login')
        self.listaccount = reverse('user-listaccounts')
        self.user = mixer.blend('app.User', phonenumber='09111234567', password='1234', is_active=True)
        self.user.password = make_password(self.user.password)
        self.user.save(update_fields=["password"])

    def test_app_model_create_user(self):
        self.assertEquals(str(self.user), self.user.phonenumber)
