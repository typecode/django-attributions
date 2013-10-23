

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


def object_from_global_id(global_id):
    app_label, model, id = global_id.split('.')
    ct = ContentType.objects.get(app_label=app_label, model=model)
    return ct.get_object_for_this_type(id=id), ct


def object_to_global_id(obj):
    return '{app_label}.{model}.{id}'.format(
        app_label=obj._meta.app_label,
        model=obj._meta.module_name,
        id=obj.id,
    )


class GlobalIdModel(models.Model):
    class Meta:
        abstract = True

    @property
    def global_id(self):
        return object_to_global_id(self)


class RootField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs['related_name'] = 'attributions'
        super(RootField, self).__init__(*args, **kwargs)


class Attribution(models.Model):
    # root = RootField(SomeRootModel)

    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    related = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{}: {} -> {}: {}'.format(type(self.root).__name__, self.root,
                                          type(self.related).__name__,
                                          self.related)

    @property
    def global_id(self):
        return object_to_global_id(self)
