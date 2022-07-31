from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from base.serializer.serializer_content import ContentSerializer


class ContentView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)

    def post(self, request):
        data = {'id': request.user.pk,
                'filename': request.data['file'].name,
                'library': request.data['library'],
                'type': request.data['type'],
                'file': request.data['file']}
        serializer = ContentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Content created successfully.'}, status=status.HTTP_200_OK)

