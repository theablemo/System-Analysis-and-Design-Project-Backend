from rest_framework.serializers import ModelSerializer
from content.models import Content


class ContentInfoSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ContentInfoSerializer, self).to_representation(instance)
        data['file_download_name'] = data['file'].split('/')[-1]
        return data
