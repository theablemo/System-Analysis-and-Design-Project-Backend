import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from backend import settings


def get_token_for_user(user):
    # gets a member and generate a new jwt token for it
    data = {}
    refresh = TokenObtainPairSerializer.get_token(user=user)
    data['refreshToken'] = str(refresh)
    data['token'] = str(refresh.access_token)
    data['validUntil'] = jwt.decode(data['token'], settings.SECRET_KEY, settings.SIMPLE_JWT['ALGORITHM']).get('exp')
    return data

