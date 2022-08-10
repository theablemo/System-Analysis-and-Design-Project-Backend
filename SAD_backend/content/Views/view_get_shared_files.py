from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import FileAccess, Content
from content.serializer import ContentInfoSerializer


class GetSharedFiles(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contents_id = FileAccess.objects.filter(shared_with=request.user).values_list('content', flat=True)
        contents = Content.objects.filter(id__in=contents_id)
        contents_info = ContentInfoSerializer(contents, context={'request': request}, many=True).data
        return Response({'info': contents_info, 'code': 'OK'})
