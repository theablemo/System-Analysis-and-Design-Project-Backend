from rest_framework import serializers
from content.models.content import Library



class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'name', 'date_created', 'type_id']



