from .models import Image, Colors
from .forms import ImageUploadForm
from django.contrib import admin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageUploadForm
    fields = ('image', 'preview_image', 'image_hash', 'colors', 'tags', 'author', 'status')


admin.site.register(Colors)
