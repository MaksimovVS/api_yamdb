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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
        "is_staff",
        "is_superuser",
        "password",
    )
    search_fields = ("username",)
    empty_value_display = ("-пусто-",)
