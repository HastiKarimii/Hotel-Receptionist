from django.contrib import admin

from .models import Receptionist


@admin.register(Receptionist)
class CustomAdmin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            return [(None, {'fields': ('username', 'password')}),
                    ('Personal info', {'fields': ('email', 'first_name', 'last_name')}),
                    (
                        'Permissions',
                        {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                    ('Important dates', {'fields': ('last_login', 'date_joined')}),
                    ('Contact info', {'fields': ('contact_no',)})
                    ]

        else:
            perm_fields = ('is_active', 'is_staff')
            return [('General Info', {'fields': ('username',)}),
                    ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                    ('Permissions', {'fields': ('is_active', 'is_staff', 'groups')})]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)


# admin.site.register(Receptionist)
