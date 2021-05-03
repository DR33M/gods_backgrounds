import os

from unidecode import unidecode
from taggit.managers import TaggableManager

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django.db.models.signals import m2m_changed, pre_save

import logging

logger = logging.getLogger(__name__)


class Color(models.Model):
    class Meta:
        verbose_name_plural = "Colors"

    hex = models.CharField(max_length=7, unique=True)
    similar_color = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.hex


class ImageFollowers(models.Model):
    class Vote(models.IntegerChoices):
        DOWNVOTE = -1
        DEFAULT = 0
        UPVOTE = 1

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=Vote.choices, default=Vote.DEFAULT)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Image(models.Model):
    class Status(models.IntegerChoices):
        MODERATION = 0
        APPROVED = 1

    title = models.CharField(max_length=50, blank=True)

    image = models.ImageField(upload_to='images/%Y/%m/%d/full_size/')
    preview_image = models.ImageField(upload_to='images/%Y/%m/%d/preview_size/', blank=True)
    image_hash = models.CharField(max_length=255, blank=True)

    colors = models.ManyToManyField(Color, blank=True)

    tags = TaggableManager()
    slug = models.SlugField(unique=True, blank=True)

    rating = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)

    width = models.IntegerField(default=0, blank=True)
    height = models.IntegerField(default=0, blank=True)
    ratio = models.FloatField(default=0, blank=True)
    size = models.CharField(max_length=255, blank=True)
    extension = models.CharField(max_length=255, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None,
                                  related_name="moderator_id", blank=True)
    followers = models.ManyToManyField(ImageFollowers, blank=True, related_name='image')
    status = models.IntegerField(choices=Status.choices, default=Status.MODERATION)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.url

    def get_slug(self):
        self.slug = slugify('-'.join([unidecode(str(a)) for a in sorted(self.tags.all())]))
        try:
            image = Image.objects.get(slug=self.slug)
            self.slug += "-" + str(self.id)
        except Image.DoesNotExist:
            pass

        return self.slug

    def get_absolute_url(self):
        return reverse('main:detailed_image_view', kwargs={'slug': self.slug})

    def delete(self, *args, **kwargs):
        super(Image, self).delete(*args, **kwargs)
        os.remove(self.image.path)
        os.remove(self.preview_image.path)


class Report(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


@receiver(m2m_changed, sender=Image.tags.through)
def create_slug_name(sender, instance, action, **kwargs):
    if action == 'post_add':
        instance.get_slug()
        instance.save()


@receiver(pre_save, sender=Image)
def copy_image(sender, instance, **kwargs):
    if not instance.preview_image:
        copied_file = ContentFile(instance.image.file.read())
        copied_file.name = instance.image.file.name
        instance.preview_image = copied_file

