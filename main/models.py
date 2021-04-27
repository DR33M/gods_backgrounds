import extcolors
from PIL import Image as PIL_Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from unidecode import unidecode
from main.utils.colors import convert_hex_color_to_name


class Color(models.Model):
    class Meta:
        verbose_name_plural = "Colors"

    hex = models.CharField(max_length=7, unique=True)
    similar_color = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.hex


class Image(models.Model):
    class Status(models.IntegerChoices):
        MODERATION = 0
        APPROVED = 1

    image = models.ImageField(upload_to='images/%Y/%m/%d/full_size/')
    preview_image = models.ImageField(upload_to='images/%Y/%m/%d/preview_size/', blank=True)
    image_hash = models.CharField(max_length=255, blank=True)

    colors = models.ManyToManyField(Color, blank=True)

    tags = TaggableManager()
    slug = models.SlugField(unique=True, blank=True)

    rating = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)

    width = models.IntegerField()
    height = models.IntegerField()
    ratio = models.IntegerField()

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

    def delete(self, *args, **kwargs):
        super(Image, self).delete(*args, **kwargs)
        self.image.storage.delete(self.image.path)
        self.preview_image.storage.delete(self.preview_image.path)

    def save(self):
        image_file = PIL_Image.open(self.image)
        self.height, self.width = image_file.height, image_file.width
        self.ratio = ratio = image_file.height / image_file.width

        super().save()

        if image_file.width > settings.IMAGE_PREVIEW_WIDTH:
            output_size = (settings.IMAGE_PREVIEW_WIDTH, round(ratio * settings.IMAGE_PREVIEW_WIDTH))
            image_file = image_file.resize(output_size)
            image_file.save(self.preview_image.path)

        image_colors, pixel_count = extcolors.extract_from_image(image_file)

        colors = Color.objects.all().values_list('hex', flat=True)

        hex_colors = []
        add_colors = []
        for image_color in image_colors:
            if (image_color[1] / pixel_count) * 100 > settings.IMAGE_MINIMUM_PERCENTAGE_OF_DOMINANT_COLORS:
                color = '#%02x%02x%02x' % image_color[0]
                hex_colors.append(color)
                if color not in colors:
                    add_colors.append(Color(hex=color, similar_color=convert_hex_color_to_name(color)))

        Color.objects.bulk_create(add_colors)
        self.colors.add(*Color.objects.filter(hex__in=hex_colors))


class UserImage(models.Model):
    class Vote(models.IntegerChoices):
        DOWNVOTE = -1
        DEFAULT = 0
        UPVOTE = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=Vote.choices, default=Vote.DEFAULT)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.pk)


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

