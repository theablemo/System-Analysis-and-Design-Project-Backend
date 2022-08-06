from datetime import datetime

import pytz
from rest_framework import serializers, status

from account.models import Member
from base.models import Library, ContentType, Content


class ContentSerializer(serializers.Serializer):
    filename = serializers.CharField()
    member_id = serializers.CharField(source='member.id')
    date_created = serializers.DateTimeField(default=datetime.fromtimestamp(0, tz=pytz.UTC))
    type = serializers.CharField(source='type.name')
    library = serializers.CharField(source='library.name')
    file = serializers.FileField()

    def validate(self, data):
        if not Library.objects.filter(name=data['library']['name']).exists():
            raise serializers.ValidationError(detail={"message": "Library not found"}, code=status.HTTP_404_NOT_FOUND)
        if not ContentType.objects.filter(name=data['contenttype']['name']).exists():
            raise serializers.ValidationError(detail={"message": "Type not found"}, code=status.HTTP_404_NOT_FOUND)
        return data

    def create(self, validated_data):
        member = Member.objects.get(pk=validated_data['member']['id'])
        library = Library.objects.get(name=validated_data['library']['name'])
        content_type = ContentType.objects.get(name=validated_data['contenttype']['name'])
        file = validated_data['file']
        content = Content.objects.create(
            filename=file.name,
            member=member,
            type=content_type,
            library=library,
            file=file
        )
        return content

    def update(self, instance, validated_data):
        if 'library' in validated_data:
            instance.library = Library.objects.get(name=validated_data['library'])
        instance.save()
        return instance
