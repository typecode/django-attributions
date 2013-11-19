

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from attributions.forms import RelatedField


class RootInline(admin.TabularInline):
    relatives = []
    ct_field = 'content_type'
    ct_fk_field = 'object_id'

    def get_formset(self, request, obj=None, **kwargs):
        fs = super(RootInline, self).get_formset(request, obj=obj, **kwargs)

        old_init = fs.form.__init__

        def __init__(form, *args, **kwargs):
            attr = kwargs.get('instance', None)
            if attr:
                initial = kwargs.get('initial', {})
                initial.update({self.ct_fk_field: attr.related.global_id})
                kwargs['initial'] = initial

            old_init(form, *args, **kwargs)

        fs.form.__init__ = __init__

        ct_field = fs.form.base_fields[self.ct_field]

        if self.relatives:
            q = Q()

            for app, model in self.relatives:
                q |= Q(app_label=app.lower(), model=model.lower())

            ct_field.queryset = ContentType.objects.filter(q)

        choice_field = RelatedField(ct_field.queryset, label='Object')
        fs.form.base_fields[self.ct_fk_field] = choice_field

        return fs


class RelatedInline(generic.GenericTabularInline):
    pass
