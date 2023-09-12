from django.urls import reverse
from mixer.backend.django import mixer
from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.hashers import make_password, check_password
import json
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User, AnonymousUser
from product.models import Product
from app import token
from app.models import User
from app.views import AccountViewset


class TestAppView(TestCase):
    def setUp(self):
        self.client = Client()
        self.create = reverse('product-createproduct')
        self.login = reverse('user-login')
        self.delete = reverse('product-deleteproduct')
        self.list = reverse('product-listproduct')
        self.edit = reverse('product-editproduct', kwargs={'pk': 1})
        self.product = mixer.blend('product.Product', name='first')
        self.user = mixer.blend('app.User', phonenumber='09111234567', password='1234', is_shop_owner=True)
        self.user.password = make_password(self.user.password)
        self.user.save(update_fields=["password"])
        self.user1 = mixer.blend('app.User', phonenumber='09121234567', password='1234')
        self.user1.password = make_password(self.user1.password)
        self.user1.save(update_fields=["password"])

    def test_view_createproduct_is_shop_owner(self):
        get_token = token.get_tokens_for_user(User.objects.get(phonenumber=self.user.phonenumber))
        response = self.client.post(self.login, {'phonenumber': '09111234567', 'password': '1234'})

        if response.status_code == 200:
            response = self.client.post(self.create, data={'name': 'first', 'inventory': True, 'price': 20000},
                                        headers={'Authorization': 'Bearer ' + str(get_token['access'])})
            self.assertEquals(response.status_code, 201)

            response = self.client.post(self.create, data={'inventory': True, 'price': 20000},
                                        headers={'Authorization': 'Bearer ' + str(get_token['access'])})
            self.assertEquals(response.status_code, 400)

            self.assertEquals(response.json()['data']['name'], ['This field is required.'])
        else:
            self.assertEquals(response.status_code, 401)
            self.assertEquals(response.json()['detail'], 'Authentication credentials were not provided.')

    def test_view_createproduct_is_not_shop_owner(self):
        get_token = token.get_tokens_for_user(User.objects.get(phonenumber=self.user1.phonenumber))
        response = self.client.post(self.login, {'phonenumber': '09121234567', 'password': '1234'})
        if response.status_code == 200:
            response = self.client.post(self.create, data={'name': 'first', 'inventory': True, 'price': 20000},
                                        headers={'Authorization': 'Bearer ' + str(get_token['access'])})
            self.assertEquals(response.status_code, 403)
            self.assertEquals(response.json()['message'], 'you dont have permission to add product')
        else:
            self.assertEquals(response.status_code, 401)
            self.assertEquals(response.json()['detail'], 'Authentication credentials were not provided.')

    def test_view_deleteproduct_is_shop_owner(self):
        get_token = token.get_tokens_for_user(User.objects.get(phonenumber=self.user.phonenumber))
        response = self.client.post(self.login, {'phonenumber': '09111234567', 'password': '1234'})
        if response.status_code == 200:
            response = self.client.delete(self.delete, data={'id': 1},
                                        headers={'Authorization': 'Bearer ' + str(get_token['access'])})
            print(response.json())
            self.assertEquals(response.status_code, 200)

            response = self.client.delete(self.delete, data={'id': 2},
                                        headers={'Authorization': 'Bearer ' + str(get_token['access'])})
            self.assertEquals(response.status_code, 404)
        else:
            self.assertEquals(response.status_code, 401)
            self.assertEquals(response.json()['detail'], 'Authentication credentials were not provided.')

    def test_view_deleteproduct_is_not_shop_owner(self):
        get_token = token.get_tokens_for_user(User.objects.get(phonenumber=self.user1.phonenumber))
        response = self.client.post(self.login, {'phonenumber': '09121234567', 'password': '1234'})
        if response.status_code == 200:
            response = self.client.delete(self.delete, data={'id': 1},
                                        headers={'Authorization': 'Bearer ' + str(get_token['access'])})
            self.assertEquals(response.status_code, 403)
            self.assertEquals(response.json()['message'], 'you dont have permission to delete product')
        else:
            self.assertEquals(response.status_code, 401)
            self.assertEquals(response.json()['detail'], 'Authentication credentials were not provided.')
