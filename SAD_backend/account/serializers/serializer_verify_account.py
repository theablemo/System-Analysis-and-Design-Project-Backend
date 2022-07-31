from rest_framework import serializers


class VerifyAccountSerializer(serializers.Serializer):
    username = serializers.EmailField(allow_blank=False)
    code = serializers.IntegerField()
