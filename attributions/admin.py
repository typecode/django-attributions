

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


class RootInline(admin.TabularInline):
    relatives = []
    ct_field = 'content_type'
    ct_fk_field = 'object_id'

    def __init__(self, *args, **kwargs):
        super(RootInline, self).__init__(*args, **kwargs)

        q = Q()
        if self.relatives:
            for rel in self.relatives:
                q |= Q(app_label=rel[0], model=rel[1])

            self.relatives = ContentType.objects.filter(q)
        else:
            self.relatives = None

    def get_formset(self, request, obj=None, **kwargs):
        fs = super(RootInline, self).get_formset(request, obj=obj, **kwargs)

        if self.relatives is not None:
            fs.form.base_fields[self.ct_field].queryset = self.relatives

        return fs


class RelatedInline(generic.GenericTabularInline):
    pass
