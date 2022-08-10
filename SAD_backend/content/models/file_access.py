from django.db import models

from account.models import Member
from content.models import Content


class FileAccess(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='owner')
    shared_with = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='shared_with')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='shared_content')

    @classmethod
    def does_member_have_access(cls, member, content):
        return content.member == member or FileAccess.objects.filter(owner=content.member, shared_with=member, content=content).exists()
