from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import Library, Content


class AddContentToLibraryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        library_name = request.data.get('library_name')
        content_id = request.data.get('content_id')

        try:
            library = Library.objects.get(name=library_name, member=request.user)
            content = Content.objects.get(id=content_id)
            if content.member != request.user:
                return Response({'message': f'you can only edit your own content.', 'code': 'ERROR'},
                                status=401)
        except Library.DoesNotExist:
            return Response({'message': f'library with name={library_name} does not exist.', 'code': 'ERROR'},
                            status=401)
        except Content.DoesNotExist:
            return Response({'message': f'content with id={content_id} does not exist.', 'code': 'ERROR'}, status=401)

        content.library = library
        content.save()

        Content.objects.filter(father_content=content_id).update(library=library)
        return Response({'code': 'OK'})
