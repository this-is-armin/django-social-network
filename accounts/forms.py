from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from sparks.models import Spark

import re


User = get_user_model()


def form_field_validator(field_name, value):
    if not value:
        return None
    
    if not re.fullmatch(r'^[a-z0-9_.]+$', value):
        raise ValidationError(f'{field_name} must contain only lowercase letters, numbers, underline and dot')
    return value


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = User
        fields = AdminUserCreationForm.Meta.fields + ('bio', 'image',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class RegisterForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'form-control',
    }))
    email = forms.EmailField(label='', max_length=100, widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email Address',
        'class': 'form-control',
    }))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your First Name',
        'class': 'form-control',
    }))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Last Name',
        'class': 'form-control',
    }))
    password = forms.CharField(label='', min_length=4, max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(label='', min_length=4, max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        form_field_validator('Username', username)

        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already exists')
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return form_field_validator('First Name', first_name)
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return form_field_validator('Last Name', last_name)
    
    def clean(self):
        cd = super().clean()
        password = cd.get('password')
        confirm_password = cd.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'form-control',
    }))
    password = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': 'form-control',
    }))


class EditAccountForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'form-control',
    }))
    email = forms.EmailField(label='', max_length=100, widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email Address',
        'class': 'form-control',
    }))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your First Name',
        'class': 'form-control',
    }))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Last Name',
        'class': 'form-control',
    }))
    bio = forms.CharField(label='', max_length=100, required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Your Bio',
        'class': 'form-control',
    }))
    image = forms.ImageField(
        label='', 
        max_length=100,
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        }),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return form_field_validator('First Name', username)
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return form_field_validator('Last Name', first_name)
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return form_field_validator('Last Name', last_name)


class DeleteAccountForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'form-control',
    }))


class AddSparkForm(forms.ModelForm):
    class Meta:
        model = Spark
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your spark...',
                'class': 'form-control',
            }),
        }