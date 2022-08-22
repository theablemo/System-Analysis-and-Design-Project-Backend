from rest_framework import serializers
from content.models.content import Library, Content


class LibraryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

    def to_representation(self, instance):
        data = super(LibraryInfoSerializer, self).to_representation(instance)
        data['content_count'] = Content.objects.filter(library=instance).count()
        return data