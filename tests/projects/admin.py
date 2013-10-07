

from django.contrib import admin

from attributions.admin import RelatedInline

from permissions.models import Permission

from .models import Project


class PermissionInline(RelatedInline):
    model = Permission
    can_delete = False


class ProjectAdmin(admin.ModelAdmin):
    inlines = (PermissionInline,)

admin.site.register(Project, ProjectAdmin)
