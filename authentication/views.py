from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import SignUpSerializer
from authentication.renderers import UserJsonRender


class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserJsonRender, )

    def post(self, request):
        data = request.data.get('user', {})
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
