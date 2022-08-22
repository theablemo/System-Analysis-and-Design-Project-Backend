from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import Library, Content
from content.serializer import ContentInfoSerializer


class GetLibraryFiles(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        library_name = request.GET.get('library_name')

        try:
            library = Library.objects.get(name=library_name, member=request.user)
        except Library.DoesNotExist:
            return Response({'message': f'library with name={library_name} does not exist.', 'code': 'ERROR'},
                            status=401)

        contents = Content.objects.filter(library=library)

        contents_info = ContentInfoSerializer(contents, context={'request': request}, many=True).data
        return Response({'info': contents_info, 'code': 'OK'})
