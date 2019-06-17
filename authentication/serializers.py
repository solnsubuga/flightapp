
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentication.identity import IdentityManager


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # Make email field for validation
    email = serializers.EmailField(
        required=True
    )

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        ''' Check if email is not already in use
        '''
        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError('Email already in use')
        return email

    def create(self, validated_data):
        ''' Create a new user '''
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


class SignInSerializer(serializers.Serializer):
    '''Signin user view '''
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        '''Validates user details and authenticates them '''
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # TODO:(solo) Check if the user is active
            identity_manager = IdentityManager()
            payload = {
                'sub': user.pk,
                'email': user.email,
                'id': user.pk,
                'username': user.username,
            }
            token = identity_manager.encode(
                payload, settings.TOKEN_EXPIRATION_TIME)
            user.last_login = timezone.now()
            user.save()
            return {
                'username': username,
                'token': token
            }
        raise AuthenticationFailed('Wrong username or password', 401)
