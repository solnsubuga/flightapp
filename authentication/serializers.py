from django.contrib.auth.models import User
from rest_framework import serializers


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
        ''' Check if email is not already in use'''
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
