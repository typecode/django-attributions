

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class RootInline(admin.TabularInline):
    relatives = []

    def __init__(self, *args, **kwargs):
        super(RootInline, self).__init__(*args, **kwargs)

        self.relatives = [
            ContentType.objects.get(app_label=rel[0], model=rel[1])
            for rel in self.relatives
        ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(RootInline, self).get_form(request, obj, **kwargs)
        # form.fields['content_type']. =

        return form


class RelatedInline(generic.GenericTabularInline):
    pass
