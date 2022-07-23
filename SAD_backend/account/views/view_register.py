from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import RegisterSerializer
from account.util.token_generator import get_token_for_user


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)

        return Response({
             "token": get_token_for_user(user),
             "code": "OK"})

