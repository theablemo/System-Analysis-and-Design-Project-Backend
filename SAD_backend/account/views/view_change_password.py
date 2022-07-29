from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models.member import Member
from account.serializers.serializer_change_password import ChangePasswordSerializer
from backend import settings
import jwt
from account.util.email_handler import send_change_password_email


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer, responses={200: {}})
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if old_password == new_password:
            return Response(status=400, data={"message": "new password and old password can not be same"}, exception=True)

        access_token = request.headers['X-token']
        user_id = jwt.decode(access_token, settings.SECRET_KEY,
                             settings.SIMPLE_JWT['ALGORITHM']).get('user_id')

        try:
            username = Member.objects.filter(
                id=user_id).values_list('username', flat=True)[0]
            authenticate(username=username, password=old_password)
            new_password_hash = make_password(new_password)

            try:
                Member.objects.filter(id=user_id).update(
                    password=new_password_hash)
                send_change_password_email(username, new_password)
                return Response(data={"message": "password changed successfully!"})

            except:
                return Response(status=400, data={"message": "please retry the action"})

        except:
            return Response(status=403, data={"message": "the old password is incorrect"})
