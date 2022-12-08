# users/admin.py

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from users.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )
    list_editable = (
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
