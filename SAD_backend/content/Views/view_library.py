from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

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

