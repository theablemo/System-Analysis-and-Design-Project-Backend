from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Member
from content.models import Content, FileAccess, Library


class GrantPermissionLibrary(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        library_name = request.data.get('library_name')

        try:
            shared_with = Member.objects.get(username=username)
            library = Library.objects.get(name=library_name, member=request.user)
        except Member.DoesNotExist:
            return Response({'message': f'member with username={username} does not exist.', 'code': 'ERROR'},
                            status=401)
        except Library.DoesNotExist:
            return Response({'message': f'library with name={library_name} does not exist.', 'code': 'ERROR'},
                            status=401)

        if shared_with != request.user:
            for content in Content.objects.filter(library=library):
                FileAccess.objects.update_or_create(owner=request.user, shared_with=shared_with, content=content)

        return Response({'code': 'OK'})
