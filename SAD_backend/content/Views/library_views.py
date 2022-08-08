from rest_framework.views import APIView
from content.serializer.library_serializer import LibrarySerializer
from content.models.content import Library
from rest_framework.response import Response

class LibraryView(APIView):

    def post(self,request):
        serializer = LibrarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            print(serializer.validated_data)
            serializer.create(serializer.validated_data)
            return Response(
                status=201,
                data= {"message":"created successfully!"}
            )
        except:
            return Response(
                status=404,
                data={
                    "message":"invalid content type id"
                }
            )

    def get(self,request):
        libraries = Library.objects.all()
        serializer = LibrarySerializer(libraries,many=True)
        return Response(serializer.data)


class LibraryDetailView(APIView):

    def get(self,request,pk):
        try:
           library_model = Library.objects.get(pk=pk)
           serializer = LibrarySerializer(data=library_model)
           return Response(
            status=200,
            data=serializer.data
           )
        except:
            return Response(
                status=404,
                data = {
                    "message":"not found!"
                }
            )