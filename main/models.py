from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.files.base import ContentFile
from PIL import Image as Img
import logging

from unidecode import unidecode

logger = logging.getLogger(__name__)


class Image(models.Model):
    class Status(models.IntegerChoices):
        MODERATION = 0
        APPROVED = 1

    image = models.ImageField(upload_to='images/%Y/%m/%d/full_size/')
    preview_image = models.ImageField(upload_to='images/%Y/%m/%d/preview_size/', blank=True)
    tags = TaggableManager()
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None,
                                  related_name="moderator_id", blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.MODERATION)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.url

    def get_slug(self):
        self.slug = slugify('-'.join([unidecode(str(a)) for a in self.tags.all()]))
        try:
            image = Image.objects.get(slug=self.slug)
            self.slug += "-" + str(self.id)
        except Image.DoesNotExist:
            pass

        return self.slug

    def get_absolute_url(self):
        return reverse('main:detailed_image_view', kwargs={'slug': self.slug})

    def save(self):
        super().save()
        img = Img.open(self.preview_image.path)

        if img.height > 1000 or img.width > 1000:
            output_size = (round(img.height / 10), round(img.width / 10))
            img.thumbnail(output_size)
            img.save(self.preview_image.path)


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
