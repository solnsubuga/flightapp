import coreapi
from django.contrib.auth.models import User
from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, exceptions

from authentication.serializers import (
    SignUpSerializer, SignInSerializer, ProfileSerializer)
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


class RetrieveUpdateFlightPassengerView(generics.RetrieveUpdateAPIView):
    '''Get/Edit user profile '''
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'passport_photo': user.profile.passport_photo,
            'passport_number': user.profile.passport_number,
            'birth_date': user.profile.birth_date,
            'citizenship': user.profile.citizenship,
        }

    def update(self, request, format=None, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
