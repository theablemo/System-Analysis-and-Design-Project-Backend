from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from content.serializer import ContentInfoSerializer
from content.serializer.serializer_content import ContentSerializer


class ContentView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
<<<<<<< HEAD:SAD_backend/content/views.py
        serializer.save()
        return Response({'message': 'Content created successfully.'}, status=status.HTTP_200_OK)
=======
        content = serializer.save()
        content_info = ContentInfoSerializer(content, context={'request': request}).data

        return Response({'info': content_info, 'code': 'OK'})
>>>>>>> master:SAD_backend/content/views/view_add_content.py
