from .models import Image, Color, UserImage
from .forms import ImageUploadForm
from django.contrib import admin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageUploadForm
    fields = ('image', 'preview_image', 'image_hash', 'colors', 'tags', 'rating', 'downloads', 'author', 'moderator', 'status')
    list_display = ('image', 'slug', 'rating', 'downloads', 'author', 'moderator', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('slug', 'tags__name',)
    ordering = ('status', 'updated_at')
    actions = ['approve_images', 'moderate_images']

    def approve_images(self, request, queryset):
        queryset.update(moderator=request.user, status=Image.Status.APPROVED)

    def moderate_images(self, request, queryset):
        queryset.update(moderator=None, status=Image.Status.MODERATION)

    approve_images.short_description = 'Approve selected images'
    moderate_images.short_description = 'Moderate selected images'


admin.site.register(Color)
admin.site.register(UserImage)
