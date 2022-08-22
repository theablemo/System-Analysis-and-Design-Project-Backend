from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from account.models.member import Member
from account.util.email_handler import send_register_email
from account.util.redis_connection import connection
from account.serializers.serializer_verify_account import VerifyAccountSerializer


class VerifyView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=VerifyAccountSerializer, responses={200: {}})
    def put(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        code = serializer.validated_data['code']
        saved_code = connection.get(username)
        if not code:
            return Response({
                "message": "username not found.",
                "code": "ERROR"}, status=400)

        if code != int(saved_code):
            return Response({
                "message": "verification code is not correct.",
                "code": "ERROR"}, status=400)

        try:
            member = Member.objects.get(username=username, verified=False)
            member.verified = True
            member.save()
            return Response({
                "message": "user verified.",
                "code": "OK"})
        except Member.DoesNotExist:
            return Response({
                "message": "user not found or already verified.",
                "code": "ERROR"}, status=400)

    def get(self, request):
        username = request.GET.get('username', None)
        if not username or not Member.objects.filter(username=username).exists():
            return Response(status=404, data={"message": "user not found"})
        send_register_email(username)
        return Response({
            "message": "verify code has been sent to your email.",
            "code": "OK"})

