from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from authentication.models import User
from authentication.serializers import SignUpSerializer
from faker import Faker


class SignUpAPIView(APITestCase):
    '''Test Module for signing up a user'''
    # pylint: disable=E1101

    def setUp(self):
        self.url = reverse('auth:signup')
        self.faker = Faker()

    def test_signup_user(self):
        username = self.faker.word()
        response = self.client.post(self.url, {
            'user': {
                'username': username,
                'email': self.faker.email(),
                'password': self.faker.password()
            }
        })

        user = User.objects.filter(username=username).first()
        serializer = SignUpSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_with_already_used_email(self):
        email = self.faker.email()
        User.objects.create_user(
            self.faker.word(), email, self.faker.password())

        response = self.client.post(self.url, {
            'user': {
                'username': self.faker.word(),
                'email': email,
                'password': self.faker.password()
            }
        })
        self.assertEqual('Email already in use',
                         response.data['errors']['email'][0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_invalid_email(self):
        response = self.client.post(self.url, {
            'user': {
                'username': self.faker.word(),
                'email': self.faker.email().strip('.com'),
                'password': self.faker.password()
            }
        })
        self.assertEqual('Enter a valid email address.',
                         response.data['errors']['email'][0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_required_fields(self):
        '''Test username, email and password are required'''
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('This field is required.',
                         response.data['errors']['username'][0])
        self.assertEqual('This field is required.',
                         response.data['errors']['email'][0])
        self.assertEqual('This field is required.',
                         response.data['errors']['password'][0])
