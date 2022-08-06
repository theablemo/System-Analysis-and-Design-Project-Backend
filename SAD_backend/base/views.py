import mimetypes

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import Content
from base.serializer.serializer_content import ContentSerializer


class ContentView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = {'member_id': 1,
                'filename': request.data['file'].name,
                'library': request.data['library'],
                'type': request.data['type'],
                'file': request.data['file']}
        serializer = ContentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Content created successfully.'}, status=status.HTTP_200_OK)

    def get(self, request, library, filename):
        try:
            content = Content.objects.get(
                member__id=request.user.pk,
                library__name=library,
                filename=filename
            )
            filepath = content.path
            mime_type, _ = mimetypes.guess_type(filepath)
            with open(filepath, 'r') as file:
                response = HttpResponse(file, status=status.HTTP_200_OK, content_type=mime_type)
                response['Content-Disposition'] = f'attachment; filename="{file.name.split("_")[-1]}"'
                return response
        except:
            return Response({'message': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)


class ContentListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.pk
        contents = Content.objects.filter(member__id=user_id)
        serializer = ContentSerializer(contents, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
