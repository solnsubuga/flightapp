from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ''' Profile model holds profile data about a user '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    citizenship = models.CharField(max_length=200, blank=True, null=True)

    def __repr__(self):
        '''General string representation of a profile '''
        return '<Profile {username}>'.format(username=self.user.username)
