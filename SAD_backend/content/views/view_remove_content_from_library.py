from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import Content


class RemoveContentFromLibraryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content_id = request.data.get('content_id')

        try:
            content = Content.objects.get(id=content_id)
            if content.member != request.user:
                return Response({'message': f'you can only edit your own content.', 'code': 'ERROR'},
                                status=401)
        except Content.DoesNotExist:
            return Response({'message': f'content with id={content_id} does not exist.', 'code': 'ERROR'}, status=401)

        content.library = None
        content.save()

        Content.objects.filter(father_content=content_id).update(library=None)
        if content.father_content:
            content.father_content.update(library=None)
        return Response({'code': 'OK'})
