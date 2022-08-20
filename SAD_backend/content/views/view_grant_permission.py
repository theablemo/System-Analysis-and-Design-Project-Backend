from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Member
from content.models import Content, FileAccess


class GrantPermission(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        content_id = request.data.get('content_id')

        try:
            shared_with = Member.objects.get(username=username)
            content = Content.objects.get(id=content_id, member=request.user)
        except Member.DoesNotExist:
            return Response({'message': f'member with username={username} does not exist.', 'code': 'ERROR'},
                            status=401)
        except Content.DoesNotExist:
            return Response(
                {'message': f'content with id={content_id} does not exist or is not owned by you.', 'code': 'ERROR'},
                status=401)

        if shared_with != request.user:
            FileAccess.objects.update_or_create(owner=request.user, shared_with=shared_with, content=content)

        return Response({'code': 'OK'})
