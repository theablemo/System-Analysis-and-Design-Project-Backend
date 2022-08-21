from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Content
from content.serializer import ContentInfoSerializer
from content.serializer.serializer_content import ContentSerializer


class ContentView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        content = serializer.save()
        content_info = ContentInfoSerializer(content, context={'request': request}).data

        return Response({'info': content_info, 'code': 'OK'})

    def get(self, request):
        id = request.data.get('id')
        all_content = request.data.get('all_content', False)

        if all_content:
            contents = Content.objects.filter(member=request.user)
            contents_info = ContentInfoSerializer(contents, context={'request': request}, many=True).data
            return Response({'info': contents_info, 'code': 'OK'})
        else:
            try:
                content = Content.objects.get(id=id)
            except Content.DoesNotExist:
                return Response({'message': f'content with id={id} does not exist.', 'code': 'ERROR'}, status=401)
            content_info = ContentInfoSerializer(content, context={'request': request}).data
            return Response({'info': content_info, 'code': 'OK'})

    def put(self, request):
        try:
            content = Content.objects.get(id=request.data.get('id'))
        except Content.DoesNotExist:
            return Response({'info': 'Content not found.', 'code': 'ERROR'}, status=404)

        serializer = ContentSerializer(data=request.data,
                                       instance=content,
                                       partial=True)
        if serializer.is_valid(raise_exception=True):
            new_content = serializer.save()
            content_info = ContentInfoSerializer(new_content, context={'request': request}).data
            return Response({'info': content_info, 'code': 'Ok'}, status=200)
        return Response({'info': 'Operation failed.', 'code': 'ERROR'}, status=400)
