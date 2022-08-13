from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from content.models import Content


class AddInfoToContentView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        content_id = request.data.get('id')
        try:
            content = Content.objects.get(id=content_id)
            info = json.loads(content.info)
            for key, value in request.data.get('info').items():
                info[key] = value
            content.info = json.dumps(info)
            content.save()
            return Response({'message': f'Content updated successfully.', 'code': 'OK'},
                            status=200)
        except Content.DoesNotExist:
            return Response({'message': f'Content with id {content_id} not found.', 'code': 'ERROR'},
                            status=404)
