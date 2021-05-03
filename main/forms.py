from PIL import Image as PIL_Image
import imagehash
from django import forms
from django.conf import settings
from django.core.files.images import get_image_dimensions
from dal import autocomplete
from .models import Image
import logging

logger = logging.getLogger(__name__)


class EditTagsForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('tags',)
        widgets = {
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
        fields = ('image', 'preview_image', 'image_hash', 'colors', 'tags',)
        widgets = {
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
            image_file = PIL_Image.open(image)
            # don't ask me how it work, i don't know, author of this shit-code: utorrentfilibusters@gmail.com
            cd['image_hash'] = imagehash.phash(image_file, 31).__str__()

            if Image.objects.filter(image_hash=self.cleaned_data['image_hash']).exclude(image__iexact=image).count() > 0:
                self.add_error('image', forms.ValidationError('Image already exists'))

            try:
                if image.size > settings.IMAGE_MAXIMUM_FILESIZE_IN_MB * 1024 * 1024:
                    self.add_error('image', forms.ValidationError('Maximum size is %d MB' % settings.IMAGE_MAXIMUM_FILESIZE_IN_MB))
            except AttributeError:
                pass

            width, height = image_file.width, image_file.height
            if width < settings.IMAGE_MINIMUM_DIMENSION[0] or height < settings.IMAGE_MINIMUM_DIMENSION[1]:
                self.add_error('image', forms.ValidationError('Minimum dimension is %d x %d' % settings.IMAGE_MINIMUM_DIMENSION))
        return cd

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if len(tags) < settings.IMAGE_MINIMUM_TAGS:
            raise forms.ValidationError('There must be at least %d tags' % settings.IMAGE_MINIMUM_TAGS)
        return tags
