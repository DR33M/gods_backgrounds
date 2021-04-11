from .models import Image, Colors
from .forms import ImageUploadForm
from django.contrib import admin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageUploadForm


admin.site.register(Colors)

