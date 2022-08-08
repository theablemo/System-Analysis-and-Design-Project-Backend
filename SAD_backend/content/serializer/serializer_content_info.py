from rest_framework.serializers import ModelSerializer
from content.models import Content


class ContentInfoSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
