from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(allow_blank=False)
    new_password = serializers.CharField(allow_blank=False)
