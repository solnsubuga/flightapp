from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    '''JWT Authentication backend for the api endpoints'''

    def authenticate(self, request):
        pass
