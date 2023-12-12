import os
import uuid
import shutil

from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.conf import settings



SITEFILES_DIR = os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'sitefiles'))


class Site(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def before_site_save(sender, instance, *args, **kwargs):
    if Site.objects.filter(id=instance.id).exists():  # update
        old_site = Site.objects.get(id=instance.id)
        if "/" in instance.name:
            raise Exception('Project name not allowed')
        if old_site.name != instance.name:
            if Site.objects.filter(name=instance.name).exists():
                raise Exception('Project name already exists')
            os.rename(
                os.path.join(SITEFILES_DIR, old_site.name),
                os.path.join(SITEFILES_DIR, instance.name),
            )
    else:  # create
        if "/" in instance.name:
            raise Exception('Project name not allowed')
        if os.path.exists(os.path.join(SITEFILES_DIR, instance.name)):
            raise Exception('Project name already exists')
        os.makedirs(os.path.join(SITEFILES_DIR, instance.name), exist_ok=True)


def after_site_delete(sender, instance, *args, **kwargs):
    if os.path.exists(os.path.join(SITEFILES_DIR, instance.name)):
        shutil.rmtree(os.path.join(SITEFILES_DIR, instance.name))


pre_save.connect(before_site_save, sender=Site)
post_delete.connect(after_site_delete, sender=Site)
