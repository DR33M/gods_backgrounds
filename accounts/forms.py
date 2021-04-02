from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile
import logging

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'off'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    old_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'settings-input p10px'}))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'settings-input p10px'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'settings-input p10px'}),
            'last_name': forms.TextInput(attrs={'class': 'settings-input p10px'}),
            'email': forms.TextInput(attrs={'class': 'settings-input p10px'}),
        }

    def check_password(self):
        cd = self.cleaned_data

        if self.instance.check_password(cd['old_password']):
            if cd['new_password']:
                validation_info = validate_password(cd['new_password'])
                if validation_info:
                    raise validation_info
                return True
        return False


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)
        widgets = {
            'photo': forms.FileInput(),
        }
