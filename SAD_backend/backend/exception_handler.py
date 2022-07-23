from rest_framework.exceptions import NotAuthenticated, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import APIException as rest_framework_APIException


class ApiException(rest_framework_APIException):
    def __init__(self, detail=None, code=None, description=None, status=400, field_name="Non-field"):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        detail = {field_name: [detail, ]}
        super(ApiException, self).__init__(detail, code)
        self.description = description
        self.status_code = status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    if isinstance(exc, NotAuthenticated):
        response = Response({
            'message': "NoToken",
            'code': None,
        }, status=401)
    elif isinstance(exc, InvalidToken):
        response = Response({
            'message': "WrongToken",
            'code': None,
        }, status=401)
    elif isinstance(exc, MethodNotAllowed):
        response = Response({
            'message': "MethodNotAllowed",
            'code': None,
        }, status=405)
    return response
