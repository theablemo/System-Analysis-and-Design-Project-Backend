from rest_framework import serializers


class MyRefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(allow_blank=False)
