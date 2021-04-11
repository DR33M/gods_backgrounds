from dal import autocomplete
from django import forms
from django.core.files.images import get_image_dimensions
from django.conf import settings
from taggit.forms import TagWidget

from .models import Image


class EditTagsForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('tags',)
        widgets = {
            #'tags': TagWidget(attrs={
            #    'required': True, 'placeholder': 'A comma-separated list of tags.', 'class': 'settings-input p10px'
            #}),
            'tags': autocomplete.TaggitSelect2(url='main:tags-autocomplete', attrs={
                'required': True, 'data-placeholder': 'A comma-separated list of tags.', 'class': 'settings-input p10px'
            })
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if len(tags) < settings.IMAGE_MINIMUM_TAGS:
            raise forms.ValidationError('There must be at least %d tags' % settings.IMAGE_MINIMUM_TAGS)
        return tags


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'tags')
        widgets = {
            #'tags': forms.TextInput(attrs={
            #    'required': True, 'placeholder': 'A comma-separated list of tags.', 'class': 'settings-input p10px'
            #}),
            'tags': autocomplete.TaggitSelect2(url='main:tags-autocomplete', attrs={
                'required': True, 'data-placeholder': 'A comma-separated list of tags.', 'class': 'settings-input p10px'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            try:
                if image.size > settings.IMAGE_MAXIMUM_FILESIZE_IN_MB * 1024 * 1024:
                    raise forms.ValidationError('Maximum size is %d MB' % settings.IMAGE_MAXIMUM_FILESIZE_IN_MB)
            except AttributeError:
                pass

            width, height = get_image_dimensions(image)
            if width < settings.IMAGE_MINIMUM_DIMENSION[0] or height < settings.IMAGE_MINIMUM_DIMENSION[1]:
                raise forms.ValidationError('Minimum dimension is %d x %d' % settings.IMAGE_MINIMUM_DIMENSION)

        return image

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if len(tags) < settings.IMAGE_MINIMUM_TAGS:
            raise forms.ValidationError('There must be at least %d tags' % settings.IMAGE_MINIMUM_TAGS)
        return tags
