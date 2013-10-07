

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from attributions.admin import RootInline

from .models import Permission


class PermissionAdmin(admin.ModelAdmin):
    pass


class PermissionInline(RootInline):
    model = Permission
    relatives = (
        ('projects', 'project'),
    )


class UserAdmin(DefaultUserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.inlines += [PermissionInline]

admin.site.register(Permission, PermissionAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
