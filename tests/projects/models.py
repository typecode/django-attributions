

from django.db import models

from attributions.models import GlobalIdModel, Attribution, RootField


class Project(GlobalIdModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ProjectAttribution(Attribution):
    root = RootField(Project)
