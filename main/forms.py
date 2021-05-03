from PIL import Image as PIL_Image
import imagehash
from django import forms
from django.conf import settings
from dal import autocomplete
from .models import Image, Report
import logging

logger = logging.getLogger(__name__)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'class': 'report-description'}),
        }


class FormCleanTags(forms.ModelForm):
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if len(tags) < settings.IMAGE_MINIMUM_TAGS:
            raise forms.ValidationError('There must be at least %d tags' % settings.IMAGE_MINIMUM_TAGS)
        return tags


class EditTagsForm(FormCleanTags):
    class Meta:
        model = Image
        fields = ('tags',)
        widgets = {
            'tags': autocomplete.TaggitSelect2(url='main:tags-autocomplete', attrs={
                'required': True, 'data-placeholder': 'A comma-separated list of tags.', 'class': 'settings-input p10px'
            })
        }


class ImageUploadForm(FormCleanTags):
    def __init__(self, service=None, *args, **kwargs):
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        if service:
            self.image_hash = service.get_hash()
            self.width, self.height = service.get_resolution()
            self.size = service.get_size()
            self.ratio = service.get_ratio()

    class Meta:
        model = Image
        fields = ('title', 'image', 'tags',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Photo title'}),
            'image': forms.FileInput(attrs={'id': 'input-image'}),
            'tags': autocomplete.TaggitSelect2(url='main:tags-autocomplete', attrs={
                'required': True, 'data-placeholder': 'A comma-separated list of tags.', 'class': 'settings-input'
            })
        }

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        image = cd.get('image')

        if image:
            if Image.objects.filter(image_hash=self.image_hash).exclude(image__iexact=image).count() > 0:
                self.add_error('image', forms.ValidationError('Image already exists'))

            try:
                if image.size > settings.IMAGE_MAXIMUM_FILESIZE_IN_MB * 1024 * 1024:
                    self.add_error('image', forms.ValidationError('Maximum size is %d MB' % settings.IMAGE_MAXIMUM_FILESIZE_IN_MB))
            except AttributeError:
                pass

            if self.width < settings.IMAGE_MINIMUM_DIMENSION[0] or self.height < settings.IMAGE_MINIMUM_DIMENSION[1]:
                self.add_error('image', forms.ValidationError('Minimum dimension is %d x %d' % settings.IMAGE_MINIMUM_DIMENSION))

        return cd
