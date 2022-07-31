from rest_framework_simplejwt.authentication import JWTAuthentication
from backend import settings


class CustomJWTAuthentication(JWTAuthentication):

    def get_raw_token(self, header):
        if not settings.SIMPLE_JWT['AUTH_HEADER']:
            return header
        super(CustomJWTAuthentication, self).get_raw_token(header)
