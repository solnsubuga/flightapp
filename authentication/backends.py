from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

from authentication.identity import IdentityManager


class JWTAuthentication(authentication.BaseAuthentication):
    '''JWT Authentication backend for the api endpoints'''

    def authenticate(self, request):
        token = authentication.get_authorization_header(
            request).decode('utf-8')
        if not token:
            return None
        try:
            token = token.split(' ')[1]
            identity_manager = IdentityManager()
            payload = identity_manager.decode(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e.__str__())
        try:
            user = User.objects.get(pk=payload['id'])
        # pylint: disable=E1101
        # User has method DoesNotExist
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User unauthenticated', 401)
        return user, token
