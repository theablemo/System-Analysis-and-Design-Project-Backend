from rest_framework.views import APIView
from content.serializer.library_serializer import LibrarySerializer
from content.models.content import Library
from rest_framework.response import Response
from rest_framework import viewsets
from content.utils.pagination import library_pagination
from rest_framework.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination


# class LibraryViewSet(viewsets.ModelViewSet):
#     serializer_class = LibrarySerializer
#     queryset = Library.objects.all()
#     pagination_class = library_pagination

class LibraryView(APIView, LimitOffsetPagination):

    def post(self,request):
        serializer = LibrarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            library = serializer.create(serializer.validated_data)
            return Response(
                status=201,
                data= {"library_id":library.id}
            )
        except:
            return Response(
                status=404,
                data={
                    "message":"please retry adding library"
                }
            )

    def get(self,request):
        libraries = Library.objects.all()
        result = self.paginate_queryset(libraries, request, view=self)
        serializer = LibrarySerializer(result,many=True)
        return Response(serializer.data)


class LibraryDetailView(APIView):

    def get(self,request,id):
        try:
           id = int(id)
           library_model = Library.objects.get(pk = id)
           serializer = LibrarySerializer(library_model)
           return Response(
            status=200,
            data=serializer.data
           )
        except:
            return Response(
                status=404,
                data = {
                    "message":"library not found!"
                }
            )


