import mimetypes

from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import Content


class DownloadView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    permission_classes = [IsAuthenticated]

    def get(self, request, file_path):
        try:
            file = Content.objects.get(file=f'contents/{file_path}', member=request.user).file
        except Content.DoesNotExist:
            return Response({'message': f'content with path={file_path} does not exist.', 'code': 'ERROR'}, status=401)

        mime_type, _ = mimetypes.guess_type(file.path)

        with open(file.path, 'rb') as file:
            response = HttpResponse(file, status=status.HTTP_200_OK, content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{file.name.split("_")[-1]}"'
            return response


