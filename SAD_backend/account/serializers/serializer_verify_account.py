from rest_framework import serializers


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.CharField(allow_blank=False)
    code = serializers.IntegerField()
