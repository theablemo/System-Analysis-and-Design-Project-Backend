from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from account.util.email_handler import send_change_password_email
from account.models.member import Member
from account.serializers.serializer_reset_password import ResetPasswordSerializer
from account.util.password_generator import generate_random_password
from django.contrib.auth.hashers import make_password


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ResetPasswordSerializer, responses={200: {}})
    def put(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = generate_random_password()
        try:
            hashed_pass = make_password(new_password)
            Member.objects.filter(username=email).update(password=hashed_pass)

            send_change_password_email(email, new_password)

            return Response(data={"message": "the password was reset successfully"})
        except:
            return Response(status=404, data={"message": f'the user with email {email} was not found'})
