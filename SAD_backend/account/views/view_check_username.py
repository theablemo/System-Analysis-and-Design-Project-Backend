from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Member


class CheckUsernameView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        exist = Member.objects.filter(username=username).exists()
        return Response({
            "exist": exist,
            "code": "OK"})

