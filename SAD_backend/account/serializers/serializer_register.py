from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.models import Member
from base.serializer.parse_validate import parse_validate_name


class RegisterSerializer(ModelSerializer):
    email = serializers.CharField(allow_blank=False)

    class Meta:
        model = Member
        fields = ['username', 'password', 'first_name', 'last_name', 'gender', 'email']

    def validate(self, attrs):
        attrs['first_name'] = parse_validate_name(attrs.get('first_name'), kind='first')
        attrs['last_name'] = parse_validate_name(attrs.get('last_name'), kind='last')
        attrs['password'] = make_password(attrs.get('password'))
        return super(RegisterSerializer, self).validate(attrs)
