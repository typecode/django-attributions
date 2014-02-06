

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r'^attributions.models.RootField'])
except ImportError:
    pass


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


def get_fuzzy_content_type(model):
    if isinstance(model, (str, basestring)):
        app_label, model = model.lower().split('.')
        return ContentType.objects.get(app_label=app_label, model=model)
    else:
        return ContentType.objects.get_for_model(model)


class GlobalIdModel(models.Model):
    class Meta:
        abstract = True

    @property
    def global_id(self):
        return object_to_global_id(self)


class RootField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('related_name', 'attributions')
        super(RootField, self).__init__(*args, **kwargs)


class AttributionManager(models.Manager):

    def get_content_type(self, *fuzzy_models):
        q = Q()
        for fm in fuzzy_models:
            q |= Q(content_type=get_fuzzy_content_type(fm))

        return self.filter(q)

    def get_related(self, model):
        ct = get_fuzzy_content_type(model)
        pks = self.filter(content_type=ct).values_list('object_id', flat=True)
        return ct.model_class().objects.filter(pk__in=pks)

    def get_ids(self):
        return self.values_list('object_id')


class Attribution(models.Model):
    # root = RootField(SomeRootModel)

    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    related = generic.GenericForeignKey('content_type', 'object_id')

    objects = AttributionManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{}: {} -> {}: {}'.format(type(self.root).__name__, self.root,
                                          type(self.related).__name__,
                                          self.related)

    @property
    def global_id(self):
        return object_to_global_id(self)
