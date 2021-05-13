from django import forms
from django.conf import settings

from .models import Image, Report
from .service import ImageService
import logging

from .widgets import Select2MultipleWidget

logger = logging.getLogger(__name__)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('title', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'class': 'report-description'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.image = kwargs.pop('image', None)
        super(ReportForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.user and self.image and Report.objects.filter(user=self.user, image=self.image).exists():
            raise forms.ValidationError('You have been already reported.')
        return self.cleaned_data


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
            'tags': Select2MultipleWidget(attrs={
                'required': True, 'data-placeholder': 'A comma-separated list of tags.'
            })
        }


class ImageUploadForm(FormCleanTags):
    def __init__(self, *args, **kwargs):
        self.service = ImageService()
        super(ImageUploadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Image
        fields = (
            'title', 'image', 'preview_image', 'image_hash', 'size', 'width', 'height', 'extension', 'ratio', 'tags',
        )
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Photo title'}),
            'image': forms.FileInput(attrs={'id': 'input-image'}),
            'tags': Select2MultipleWidget(attrs={
               'required': True, 'data-placeholder': 'A comma-separated list of tags.'
            })
        }

    def clean(self):
        super().clean()
        cd = self.cleaned_data

        if self.service and 'image' in cd:
            self.service = ImageService(cd['image'])
            cd['image'].file.seek(0)

            cd['image_hash'] = self.service.get_hash()
            cd['width'], cd['height'] = self.service.get_resolution()
            cd['size'] = self.service.get_size()
            cd['ratio'] = self.service.get_ratio()
            cd['extension'] = self.service.get_extension()

            if self.service.is_animated():
                self.add_error('image', forms.ValidationError('Only static images'))

            if 'image' in cd and Image.objects.filter(image_hash=cd['image_hash']).exclude(image__iexact=str(cd['image'])).count() > 0:
                self.add_error('image', forms.ValidationError('Image already exists'))

            try:
                if 'image' in cd and cd['size'] > settings.IMAGE_MAXIMUM_FILESIZE_IN_MB * 1024 * 1024:
                    self.add_error('image', forms.ValidationError('Maximum size is %d MB' % settings.IMAGE_MAXIMUM_FILESIZE_IN_MB))
            except AttributeError:
                pass

            if 'image' in cd and cd['width'] < settings.IMAGE_MINIMUM_DIMENSION[0] or cd['height'] < settings.IMAGE_MINIMUM_DIMENSION[1]:
                self.add_error('image', forms.ValidationError('Minimum dimension is %d x %d' % settings.IMAGE_MINIMUM_DIMENSION))

        return cd
