from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from account.serializers.serializer_refresh_token import MyRefreshTokenSerializer
from django.utils.translation import ugettext_lazy as _
from account.util.token_generator import token_to_json
from backend.exception_handler import ApiException


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(request_body=MyRefreshTokenSerializer, responses={200: {}})
    def post(self, request, *args, **kwargs):
        serializer = MyRefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh_token']

        ser = TokenRefreshSerializer(data={'refresh': str(refresh)})
        try:
            ser.is_valid()
            token = ser.validated_data['access']
        except TokenError:
            raise ApiException(detail=_('Token refresh error'), code="TokenRefreshError", status=400)
        return Response({
            "token": token_to_json(token, refresh),
            "code": "OK"
        })
