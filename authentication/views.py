from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import coreapi

from authentication.serializers import SignUpSerializer, SignInSerializer
from authentication.renderers import UserJsonRender
from drf_yasg.utils import swagger_auto_schema


class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserJsonRender, )

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={201: serializer_class, 400: 'Bad Request'})
    def post(self, request):
        ''' Sign up a new user
        Args:
            request(Request): HTTP request
        '''
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class SignInView(APIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={200: serializer_class, 400: 'Bad Request', 403: 'Forbidden'})
    def post(self, request):
        '''Login a user
        Args:
            request(Request): HTTP request  
        '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)
