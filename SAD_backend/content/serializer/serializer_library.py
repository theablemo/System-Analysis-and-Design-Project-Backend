from rest_framework import serializers, status
from content.models.content import Library, ContentType


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['name', 'type']

    def validate(self, data):
        super(LibrarySerializer, self).validate(data)
        if not ContentType.objects.filter(type=data['type']).exists():
            raise serializers.ValidationError(detail={"message": "Content type not found"},
                                              code=status.HTTP_404_NOT_FOUND)
        return data

    def create(self, validated_data):
        library = Library.objects.create(
            member=self.context.get("request").user,
            name=validated_data['name'],
            type=validated_data['type'],
        )
        return library
