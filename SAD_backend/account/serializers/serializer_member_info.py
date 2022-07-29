from rest_framework.serializers import ModelSerializer
from account.models import Member


class MemberInfoSerializer(ModelSerializer):

    class Meta:
        model = Member
        fields = ['username', 'first_name', 'last_name', 'gender', 'last_seen', 'is_staff']