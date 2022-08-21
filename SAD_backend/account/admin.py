from django.contrib import admin

# Register your models here.
from account.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'gender', 'last_seen', 'verified']
    list_filter = ['verified']
    sortable_by = ['id', 'email', 'last_seen']
    list_editable = ['verified']