from rest_framework.serializers import ModelSerializer
from account.models import Member


class MemberInfoSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = ['username', 'first_name', 'last_name', 'gender', 'last_seen', 'is_staff']

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        if 'gender' in validated_data:
            instance.gender = validated_data['gender']
        instance.save()
        return instance
