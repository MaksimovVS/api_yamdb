# users/admin.py

from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'is_staff',
        'is_superuser',
        'password',
    )
    search_fields = (
        'username',
    )
    empty_value_display = (
        '-пусто-',
    )
