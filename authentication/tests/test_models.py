from unittest import TestCase
from autofixture import AutoFixture
from faker import Faker
from django.contrib.auth.models import User

from authentication.models import Profile


class TestModelsTestCase(TestCase):
    def setUp(self):
        self.first_name = 'test'
        self.username = 'test'
        self.password = 'test'
        self.user = User(first_name=self.first_name, last_name=self.first_name,
                         username=self.username, password=self.password)
        self.faker = Faker()

        self.passport_number = self.faker.word()
        self.country = self.faker.country()

    def test_can_create_user(self):
        '''Test can you can actually create a user '''
        self.user.save()
        created_user = User.objects.filter(username=self.username).first()
        self.assertIsNotNone(created_user)

    def test_saving_user_creates_profile(self):
        '''Test that you when you save a user their profile is created'''
        self.user.save()
        self.assertIsNotNone(self.user.profile)

    def test_can_edit_user_profile(self):
        '''Test that you can edit a profile '''
        self.user.save()
        self.user.profile.passport_number = self.passport_number
        self.user.profile.birth_date = self.faker.date()
        self.user.profile.citizenship = self.country
        self.user.save()

        user_profile = Profile.objects.filter(user=self.user).first()

        self.assertEqual(user_profile.passport_number, self.passport_number)
        self.assertIsNotNone(user_profile.citizenship, self.country)

    def test_profile_string_representation(self):
        self.user.save()
        self.assertEqual(repr(self.user.profile), '<Profile {username}>'.format(
            username=self.user.username))

    def tearDown(self):
        User.objects.filter(username=self.username).delete()
