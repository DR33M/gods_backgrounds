from .models import Image, Color, UserImage
from .forms import ImageUploadForm
from django.contrib import admin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageUploadForm
    fields = ('image', 'preview_image', 'image_hash', 'colors', 'tags', 'rating', 'downloads', 'author', 'status')


admin.site.register(Color)
admin.site.register(UserImage)
