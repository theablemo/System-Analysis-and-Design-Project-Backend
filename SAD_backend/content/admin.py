from django.contrib import admin
from content.models import Content, FileAccess
from content.models.content import ContentType, Library


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['member_email', 'date_created', 'type_name', 'type_type', 'father_content']
    sortable_by = ['date_created']
    list_filter = ['member__email', 'type__name', 'type__type', 'father_content']

    def type_name(self, obj):
        return obj.type.name

    def type_type(self, obj):
        return obj.type.type

    def member_email(self, obj):
        return obj.member.email


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    sortable_by = ['name', 'type']
    list_filter = ['name', 'type']


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_created', 'member_email', 'type', 'content_count']
    sortable_by = ['name', 'date_created', 'member_email', 'type', 'content_count']
    list_filter = ['name', 'member__email', 'type']

    def content_count(self, obj):
        return obj.content_set.all().count()

    def member_email(self, obj):
        return obj.member.email


admin.site.register(FileAccess)
