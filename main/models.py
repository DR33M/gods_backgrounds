from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from taggit.managers import TaggableManager


class Image(models.Model):
    class Status(models.IntegerChoices):
        MODERATION = 0
        APPROVED = 1

    image = models.ImageField(upload_to='images/%Y/%m/%d')
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
        self.slug = slugify('-'.join([str(a) for a in self.tags.all()]))
        try:
            image = Image.objects.get(slug=self.slug)
            self.slug += "-" + str(self.id)
        except Image.DoesNotExist:
            pass

        return self.slug

    def get_absolute_url(self):
        return reverse('main:detailed_image_view', kwargs={'slug': self.slug})


@receiver(m2m_changed, sender=Image.tags.through)
def create_slug_name(sender, instance, action, **kwargs):
    if action == 'post_add':
        instance.get_slug()
        instance.save()
