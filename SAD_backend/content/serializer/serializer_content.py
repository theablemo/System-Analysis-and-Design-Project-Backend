from datetime import datetime
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer
from content.models.content import ContentType, Content, Library


class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = ['file', 'father_content', 'library', 'info']

    def validate(self, data):
        super(ContentSerializer, self).validate(data)
        type_name = data['file'].name.split('.')[-1]
        if not ContentType.objects.get(name=type_name):
            raise serializers.ValidationError(detail={"message": "Content type not found"},
                                              code=status.HTTP_404_NOT_FOUND)

        if 'father_content' in data:
            if not data['father_content'].type.is_compatible_as_attachment(type_name):
                raise serializers.ValidationError(
                    detail={"message": "attachment type not compatible with father content"},
                    code=status.HTTP_400_BAD_REQUEST)
            if 'library' in data and data['library'] != data['father_content'].library:
                raise serializers.ValidationError(
                    detail={"message": "attachment should be in the same library as father content"},
                    code=status.HTTP_400_BAD_REQUEST)
        if 'library' in data:
            content_type = ContentType.objects.get(name=type_name)
            if data['library'].type != content_type.type:
                raise serializers.ValidationError(
                    detail={"message": "Content and library must be of the same type."},
                    code=status.HTTP_400_BAD_REQUEST
                )

        return data

    def create(self, validated_data):
        type_name = validated_data['file'].name.split('.')[-1]
        content_type = ContentType.objects.get(name=type_name)

        content = Content.objects.create(
            member=self.context.get("request").user,
            type=content_type,
            library=validated_data.get('library'),
            file=validated_data['file'],
            father_content=validated_data.get('father_content'),
            date_created=datetime.now()
        )
        return content

    def update(self, instance, validated_data):
        if 'library' in validated_data:
            instance.library = Library.objects.get(name=validated_data['library'])
        instance.save()
        return instance
