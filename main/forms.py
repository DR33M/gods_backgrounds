import copy
from PIL import Image as PIL_Image
import imagehash
from django import forms
from django.conf import settings
from dal import autocomplete

from .models import Image, Report
from .service import ImageService
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
    def __init__(self, *args, **kwargs):
        self.service = None
        if 'files' in kwargs and 'image' in kwargs['files']:
            self.service = ImageService(copy.deepcopy(kwargs['files']['image']))
        super(ImageUploadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Image
        fields = ('title', 'image', 'preview_image', 'image_hash', 'size',  'width',  'height',  'extension', 'ratio', 'tags',)
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
        if self.service:
            cd['image_hash'] = self.service.get_hash()
            cd['width'], cd['height'] = self.service.get_resolution()
            cd['size'] = self.service.get_size()
            cd['ratio'] = self.service.get_ratio()
            cd['extension'] = self.service.get_extension()

            if Image.objects.filter(image_hash=cd['image_hash']).exclude(image__iexact=cd['image']).count() > 0:
                self.add_error('image', forms.ValidationError('Image already exists'))

            try:
                if cd['size'] > settings.IMAGE_MAXIMUM_FILESIZE_IN_MB * 1024 * 1024:
                    self.add_error('image', forms.ValidationError('Maximum size is %d MB' % settings.IMAGE_MAXIMUM_FILESIZE_IN_MB))
            except AttributeError:
                pass

            if cd['width'] < settings.IMAGE_MINIMUM_DIMENSION[0] or cd['height'] < settings.IMAGE_MINIMUM_DIMENSION[1]:
                self.add_error('image', forms.ValidationError('Minimum dimension is %d x %d' % settings.IMAGE_MINIMUM_DIMENSION))

        return cd
