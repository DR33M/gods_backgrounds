from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile
import logging

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'off'}))


class NewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def clean_password2(self):
        cd = self.cleaned_data
        if not cd['password2']:
            raise forms.ValidationError('Incorrect data')
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')

        validation_info = validate_password(cd['password'])
        if validation_info:
            self.add_error('password', validation_info)

        return cd['password2']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True, 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'required': True, 'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'required': True, 'placeholder': 'Email'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('Incorrect data')
        if len(first_name) > 20:
            raise forms.ValidationError('First name is too long')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Incorrect data')
        if len(last_name) > 30:
            raise forms.ValidationError('Last name is too long')

        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            raise forms.ValidationError('Incorrect data')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email address exists")

        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if not cd['password2']:
            raise forms.ValidationError('Incorrect data')
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')

        validation_info = validate_password(cd['password'])
        if validation_info:
            self.add_error('password', validation_info)

        return cd['password2']


class UserEditForm(forms.ModelForm):
    old_password = forms.CharField(required=False, widget=forms.PasswordInput())
    new_password = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'required': True, 'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'required': True, 'placeholder': 'Last name'
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not first_name:
            raise forms.ValidationError('Incorrect data')
        if len(first_name) > 20:
            raise forms.ValidationError('First name is too long')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if not last_name:
            raise forms.ValidationError('Incorrect data')
        if len(last_name) > 30:
            raise forms.ValidationError('Last name is too long')

        return last_name

    def clean_old_password(self):
        cd = self.cleaned_data
        data = self.data

        if data['new_password'] \
                and self.instance.has_usable_password() \
                and not self.instance.check_password(cd['old_password']):
            raise forms.ValidationError('Incorrect old password')

        return cd['old_password']

    def clean_new_password(self):
        cd = self.cleaned_data

        if cd['new_password']:
            validation_info = validate_password(cd['new_password'])
            if validation_info:
                raise validation_info

        return cd['new_password']


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={
                'required': True, 'placeholder': 'Email', 'class': 'settings-input p10px'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            raise forms.ValidationError('Incorrect data')
        if self.instance.email and not self.instance.email == email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("User with this email address exists")

        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)
        widgets = {
            'photo': forms.FileInput(attrs={'id': 'input-image'}),
        }
