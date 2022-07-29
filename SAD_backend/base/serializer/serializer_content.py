from rest_framework import serializers

from account.models import Member
from base.models import Library, ContentType, Content


class ContentSerializer(serializers.Serializer):
    filename = serializers.CharField()
    member = serializers.CharField(source='member.id')
    date_created = serializers.DateTimeField()
    type = serializers.CharField(source='contenttype.name')
    library = serializers.CharField(source='library.name')

    def validate(self, data):
        # TODO: Validate data
        return data

    def create(self, validated_data):
        member = Member.objects.get(pk=validated_data['id'])
        library = Library.objects.get(name=validated_data['library'])
        content_type = ContentType.objects.get(name=validated_data['type'])
        file = validated_data['file']
        content = Content.objects.create(
            filename=file.filename,
            member=member.objec,
            type=content_type,
            library=library
        )
        return content

    def update(self, instance, validated_data):
        # TODO: Complete update method
        pass
