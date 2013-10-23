

from django import forms
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import (ObjectDoesNotExist, PermissionDenied,
                                    ValidationError)
from django.forms.models import model_to_dict

from .models import object_from_global_id


class RootForm(forms.ModelForm):

    response_data = {}

    def __init__(self, user=None, **kwargs):
        self.user = user if user is not None else AnonymousUser()
        super(RootForm, self).__init__(**kwargs)

        self.create = kwargs.get('instance', None) is None

        for key in self.fields:
            self.fields[key].required = False

        opts = self._meta
        data = model_to_dict(self.instance, opts.fields, opts.exclude)
        data.update(self.data)
        self.data = data
        self.data.pop('id', None)

    def save(self):
        obj = super(RootForm, self).save(commit=False)

        self.response_data = self.data.copy()

        for key in self.response_data.keys():
            if not hasattr(self.instance, key):
                del self.response_data[key]

        if self.create:
            obj.save()
        else:
            obj.save(update_fields=self.response_data.keys())
            obj = type(obj).objects.get(id=obj.id)  # make sure it's updated

        return obj

    def clean(self):
        cleaned_data = super(RootForm, self).clean()
        self.is_authorized(cleaned_data)
        return cleaned_data

    def is_authorized(self, cleaned_data):
        if self.create:
            if not self._meta.model.can_create(self.user):
                raise PermissionDenied
        else:
            if not self.instance.can_edit(self.user):
                raise PermissionDenied


class AttributionForm(RootForm):

    def clean(self):
        cleaned_data = super(AttributionForm, self).clean()

        ct = cleaned_data['content_type']
        object_id = cleaned_data['object_id']

        try:
            ct.get_object_for_this_type(id=object_id)
        except ObjectDoesNotExist:
            e = 'No such attribution: {}.{}.{}'.format(ct.app_label, ct.model,
                                                       object_id)
            raise ValidationError(e)

        return cleaned_data

    def is_authorized(self, cleaned_data):
        if self.create:
            rf = self._meta.model.root_field
            if rf in cleaned_data and not cleaned_data[rf].can_edit(self.user):
                raise PermissionDenied
        else:
            if not self.instance.root.can_edit(self.user):
                raise PermissionDenied


class ReverseAttributionForm(AttributionForm):

    def is_authorized(self, cleaned_data):
        ct = cleaned_data['content_type']
        object_id = cleaned_data['object_id']

        try:
            related = ct.get_object_for_this_type(id=object_id)
            if related.can_edit(self.user):
                return
        except ObjectDoesNotExist:
            pass

        raise PermissionDenied


class RelatedField(forms.ChoiceField):

    def __init__(self, queryset, *args, **kwargs):
        kwargs['choices'] = [('', '------')]
        for ct in queryset:
            kwargs['choices'] += [
                (rel.global_id, unicode(rel))
                for rel in ct.model_class().objects.all()
            ]

        super(RelatedField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(RelatedField, self).to_python(value)
        if value:
            obj, ct = object_from_global_id(value)
            value = obj.pk

        return value
