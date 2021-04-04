from django import forms
from .models import Image


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'images-search__input p14px', 'placeholder': 'Something...'
    }))


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'tags')
        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': 'A comma-separated list of tags.'}),
        }

    def clean_tags(self):
        cd = self.cleaned_data
        if len(cd['tags']) < 3:
            raise forms.ValidationError('There must be more than two tags')
        return cd['tags']
