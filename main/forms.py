from PIL import Image
from django import forms
import imagehash
from .models import Images
import logging

logger = logging.getLogger(__name__)


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'images-search__input p14px', 'placeholder': 'Something...'
    }))


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image', 'preview_image', 'image_hash', 'colors', 'tags', 'author', 'status',)

    def clean(self):
        super().clean()
        cd = self.cleaned_data

        image_file = Image.open(cd['image'])

        if not cd['image_hash']:
            # don't ask me how it work, i don't know, author of this shit-code: utorrentfilibusters@gmail.com
            cd['image_hash'] = imagehash.phash(image_file, 31).__str__()

        if Images.objects.filter(image_hash=cd['image_hash']).count() > 0:
            self.add_error('image', forms.ValidationError('Image already exists'))

        return cd

