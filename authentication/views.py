from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import SignUpSerializer, SignInSerializer
from authentication.renderers import UserJsonRender


class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserJsonRender, )

    def post(self, request):
        ''' Handle signup POST request
        Args:
            request(Request): HTTP request
        '''
        data = request.data.get('user', {})
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class SignInView(APIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        '''Handle signin POST request 
        Args:
            request(Request): HTTP request  
        '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)
