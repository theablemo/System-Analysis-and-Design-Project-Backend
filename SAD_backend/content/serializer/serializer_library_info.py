from rest_framework import serializers
from content.models.content import Library


class LibraryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
