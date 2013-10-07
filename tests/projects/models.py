

from django.db import models

from attributions.models import Root, Attribution, RootField


class Project(Root):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ProjectAttribution(Attribution):
    root = RootField(Project)
