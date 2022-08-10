from django.contrib import admin
from content.models import Content, FileAccess
from content.models.content import ContentType, Library

admin.site.register(Content)
admin.site.register(ContentType)
admin.site.register(Library)
admin.site.register(FileAccess)