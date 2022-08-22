import json

from rest_framework.serializers import ModelSerializer
from content.models import Content
from content.models.content import ContentType


class ContentInfoSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ContentInfoSerializer, self).to_representation(instance)
        data['file_download_name'] = data['file'].split('/')[-1]
        data['type_category'] = ContentType.objects.get(id=data['type']).type
        data['has_attachment'] = Content.objects.filter(father_content=instance.id).exists()
        data['info'] = json.loads(instance.info)
        data['file_size'] = instance.file.size
        return data
