from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from account.util.token_generator import get_token_for_user
from backend.exception_handler import ApiException


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise ApiException(detail=_("username or password is incorrect."), status=400)
        token = get_token_for_user(user)
        return Response({
            "token": token,
            "verified": user.verified,
            "code": "OK"})
