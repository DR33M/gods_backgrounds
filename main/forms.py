from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'images-search__input p14px', 'placeholder': 'Something...'
    }))
