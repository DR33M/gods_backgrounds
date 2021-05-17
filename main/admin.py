from .models import Image, Color, UsersActions, Report
from .forms import ImageUploadForm
from django.contrib import admin


class UsersActionsInline(admin.TabularInline):
    model = UsersActions


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageUploadForm
    fields = (
        'title', 'image', 'preview_image', 'image_hash', 'colors', 'tags', 'slug', 'rating',
        'width', 'height', 'ratio', 'size', 'extension', 'downloads', 'author', 'moderator',
        'status'
    )
    exclude = ('users_actions',)
    list_display = ('pk', 'slug', 'rating', 'downloads', 'author', 'moderator', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('slug', 'tags__name',)
    ordering = ('pk',)
    actions = ['approve_images', 'moderate_images']

    inlines = (UsersActionsInline,)

    def approve_images(self, request, queryset):
        queryset.update(moderator=request.user, status=Image.Status.APPROVED)

    def moderate_images(self, request, queryset):
        queryset.update(moderator=None, status=Image.Status.MODERATION)

    approve_images.short_description = 'Approve selected images'
    moderate_images.short_description = 'Moderate selected images'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_id', 'user')
    list_filter = ('title', 'image_id', 'user')
    ordering = ('title', 'image_id', 'user')


@admin.register(UsersActions)
class ImageUserActionsAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'user_id', 'vote', 'downloaded',)
    list_filter = ('image_id', 'user_id', 'vote', 'downloaded',)
    ordering = ('image_id', 'user_id', 'vote', 'downloaded',)


admin.site.register(Color)
