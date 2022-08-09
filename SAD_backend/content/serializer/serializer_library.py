from rest_framework import serializers
from content.models.content import Library


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['name']

    def create(self, validated_data):
        library = Library.objects.create(
            member=self.context.get("request").user,
            name=validated_data['name']
        )
        return library
