from .models import Image, Color, ImageFollowers, Report
from .forms import ImageUploadForm, ReportForm
from django.contrib import admin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageUploadForm
    fields = ('title', 'image', 'preview_image', 'image_hash', 'colors', 'tags', 'rating', 'ratio', 'downloads', 'author', 'followers', 'moderator', 'status')
    list_display = ('pk','slug', 'rating', 'downloads', 'author', 'moderator', 'status', 'created_at', 'updated_at')
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


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    form = ReportForm
    list_display = ('title', 'image_id', 'user')
    list_filter = ('title', 'image_id', 'user')
    ordering = ('title', 'image_id', 'user')


admin.site.register(Color)
admin.site.register(ImageFollowers)
