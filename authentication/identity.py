import datetime
import jwt
from django.conf import settings


class IdentityManager():
    ''' User identity management'''

    def decode(self, token):
        '''Decode token
        Args:
            token (string): Bearer token
         '''

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
        # TODO (solo): catch all jwt exceptions and return relevant messges
        except Exception as e:
            raise Exception(e.__str__())
        else:
            return payload

    def encode(self, data, exp):
        ''' Encode data
        Args:
            data (dict): Payload to encode
            exp (int): Expires in seconds
        '''
        data.update({'iss': settings.TOKEN_ISSUER,
                     'iat': datetime.datetime.now(),
                     'exp': datetime.datetime.now() + datetime.timedelta(seconds=exp)})
        encoded = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')
        return encoded.decode('utf-8')
