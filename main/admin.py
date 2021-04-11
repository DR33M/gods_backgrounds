from .models import Images, Colors
from .forms import ImageForm
from django.contrib import admin


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    form = ImageForm


admin.site.register(Colors)

