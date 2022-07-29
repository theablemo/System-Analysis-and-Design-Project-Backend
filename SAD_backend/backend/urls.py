from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api_schema', get_schema_view(title='API schema', description='Guide for the REST API'), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url': 'api_schema'}
    ), name='swagger-ui'),
]
