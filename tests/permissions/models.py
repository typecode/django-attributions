

from django.contrib.auth.models import User
from django.db import models

from attributions.models import Attribution, RootField


class Permission(Attribution):
    root = RootField(User, verbose_name='user')

    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)



