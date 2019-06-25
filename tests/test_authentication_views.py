from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from faker import Faker

from authentication.models import User
from authentication.serializers import SignUpSerializer
from authentication.identity import IdentityManager
from tests.base_test import BaseTestCase


class SignUpAPIViewTestCase(APITestCase):
    '''Test Module for signing up a user'''
    # pylint: disable=E1101

    def setUp(self):
        self.url = reverse('auth:signup')
        self.faker = Faker()

    def test_signup_user(self):
        username = self.faker.word()
        response = self.client.post(self.url, {
            'username': username,
            'email': self.faker.email(),
            'password': self.faker.password()
        })

        user = User.objects.filter(username=username).first()
        serializer = SignUpSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_with_already_used_email(self):
        email = self.faker.email()
        User.objects.create_user(
            self.faker.word(), email, self.faker.password())

        response = self.client.post(self.url, {
            'username': self.faker.word(),
            'email': email,
            'password': self.faker.password()
        })
        self.assertEqual('Email already in use',
                         response.data['errors']['email'][0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_invalid_email(self):
        response = self.client.post(self.url, {
            'username': self.faker.word(),
            'email': 'test@',
            'password': self.faker.password()

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


class SignInAPIViewTestCase(APITestCase):
    ''' Test module for signing a user '''
    # pylint: disable=E1101

    def setUp(self):
        self.url = reverse('auth:signin')
        self.faker = Faker()
        self.username = self.faker.word()
        self.password = self.faker.password()
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def test_user_can_signin(self):
        response = self.client.post(
            self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')

    def test_valid_token_is_returned(self):
        response = self.client.post(
            self.url, {'username': self.username, 'password': self.password})
        token = response.data.get('token')
        manager = IdentityManager()
        user_details = manager.decode(token)
        self.assertEqual(self.user.pk, user_details['id'])
        self.assertEqual(self.user.username, user_details['username'])

    def test_user_signin_fails_with_wrong_credentials(self):
        response = self.client.post(
            self.url, {'username': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Wrong username or password', response.data['detail'])

    def dropDown(self):
        user = User.objects.filter(username=self.username).first()
        if user:
            user.delete()


class RetrieveUpdateFlightPassengerViewTestCase(BaseTestCase):
    # pylint: disable=E1101
    def setUp(self):
        super().setUp()
        self.url = reverse('profile')
        self.data = {
            'first_name': self.faker.word(),
            'passport_number': self.faker.word(),
            'field': ''
        }

    def test_get_user_profile(self):
        response = self.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['email'], self.user.email)

    def test_user_edit_profile(self):
        response = self.patch(self.url, self.data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(
            response.data['passport_number'], self.user.profile.passport_number)

    def test_non_existent_user_get_profile(self):
        manager = IdentityManager()
        token = manager.encode({'id': 0}, 36000)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {token}'.format(token=token))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empty_field_edit_profile(self):
        response = self.patch(self.url, {
            'email': '',
            'passport_number': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('This field may not be blank.',
                         response.data['errors']['email'][0])
        self.assertEqual('This field may not be blank.',
                         response.data['errors']['passport_number'][0])
