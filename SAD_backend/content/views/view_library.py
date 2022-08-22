from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Library
from content.serializer import LibrarySerializer, LibraryInfoSerializer


class LibraryView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LibrarySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        library = serializer.create(serializer.validated_data)

        library_info = LibraryInfoSerializer(library, context={'request': request}).data

        return Response({'info': library_info, 'code': 'OK'})

    def get(self, request):
        libraries = Library.objects.filter(member=request.user)
        library_info = LibraryInfoSerializer(libraries, context={'request': request}, many=True).data
        return Response({'info': library_info, 'code': 'OK'})

    def put(self, request):
        try:
            library = Library.objects.get(id=request.data.get('id'))
        except Library.DoesNotExist:
            return Response({'info': 'Library not found.', 'code': 'ERROR'}, status=404)
        if 'type' in request.data and request.data['type'] != library.type:
            related_contents = library.content_set.all()
            if related_contents.count() > 0:
                return Response(
                    {'info': 'You can not change type since there exist at least one content in this library '
                             'with the old type. Remove them and try again.', 'code': 'ERROR'}, status=400)
        serializer = LibrarySerializer(data=request.data,
                                       instance=library,
                                       partial=True)
        if serializer.is_valid():
            new_library = serializer.save()
            library_info = LibraryInfoSerializer(new_library, context={'request': request}).data
            return Response({'info': library_info, 'code': 'Ok'}, status=200)
        return Response({'info': 'Operation failed.', 'code': 'ERROR'}, status=400)

    def delete(self, request):
        try:
            library = Library.objects.get(id=request.GET.get('id'), member=request.user)
        except Library.DoesNotExist:
            return Response({'info': 'Library not found.', 'code': 'ERROR'}, status=404)

        library.delete()
        return Response({'code': 'Ok'}, status=200)
