from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import MemberInfoSerializer


class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={'200':MemberInfoSerializer})
    def get(self, request, *args, **kwargs):
        member_info = MemberInfoSerializer(request.user, context={'request': request}).data

        return Response({
            "info": member_info,
            "code": "OK"})

    def put(self, request):
        serializer = MemberInfoSerializer(data=request.data,
                                       instance=request.user,
                                       partial=True)

        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            content_info = MemberInfoSerializer(new_user, context={'request': request}).data
            return Response({'info': content_info, 'code': 'Ok'}, status=200)
        return Response({'info': 'Operation failed.', 'code': 'ERROR'}, status=400)