from django.contrib import admin
from authtools.admin import UserAdmin as BasicUserAdmin, BASE_FIELDS, ADVANCED_PERMISSION_FIELDS, DATE_FIELDS
from users.models import User


class UserAdmin(BasicUserAdmin):
    list_display = ('nick',
                    'english_name', 'hebrew_name',
                    'is_active', 'email', 'is_superuser', 'is_staff',)
    list_display_links = ('nick', 'english_name', 'hebrew_name', 'email')

    fieldsets = (
        BASE_FIELDS,
        (None, {
            'fields': (
                ('english_name', 'hebrew_name',),
                ('email_privacy',),
                ('biography',),
                ('github_username',)
            ),
        }),

        ADVANCED_PERMISSION_FIELDS,
        DATE_FIELDS,
    )


admin.site.register(User, UserAdmin)
