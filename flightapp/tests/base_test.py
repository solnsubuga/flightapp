from django.urls import reverse
from django.contrib.auth.models import User

from faker import Faker
from rest_framework.test import APIClient, APITestCase


class BaseTestCase(APITestCase):
     # pylint: disable=E1101
    def setUp(self):
        self.login_url = reverse('auth:signin')
        self.faker = Faker()
        self.username = self.faker.word()
        self.password = self.faker.password()
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def login(self):
        response = self.client.post(
            self.login_url, {'username': self.username, 'password': self.password})
        token = response.data.get('token')
        return token

    def post(self, url, data):
        '''Post data helper method'''
        token = self.login()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {token}'.format(token=token))
        response = self.client.post(url, data)
        return response

    def patch(self, url, data):
        '''Post data helper method'''
        token = self.login()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {token}'.format(token=token))
        response = self.client.patch(url, data)
        return response

    def get(self, url, auth=True):
        token = self.login()
        if auth:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer {token}'.format(token=token))
        response = self.client.get(url)
        return response

    def dropDown(self):
        user = User.objects.filter(username=self.username).first()
        if user:
            user.delete()
