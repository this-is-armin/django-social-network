from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import FileExtensionValidator

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('bio', 'image',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


def validate_name_field(value, field_name):
    """To validate name fields (username, first_name, last_name)"""
    INVALID_CHARS = ['(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', ',', '~', '`', '!', '?', '@', '#', '$', '%', '^', '&', '*', '-', '+', '=', ' ']
    INVALID_NAMES = ['admin', 'ADMIN']

    if not value:
        return value
    
    for char in INVALID_CHARS:        
        if char in value:
            raise ValidationError(f'Your {field_name} contains invalid character(s) or space')
    
    for name in INVALID_NAMES:
        if name == value:
            raise ValidationError(f"Your {field_name} can't be '{name}'")
        
        if name in value:
            raise ValidationError(f"Your {field_name} can't contain '{name}'")
    
    return value


class UserSignUpForm(forms.Form):
    username = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
    }))
    email = forms.EmailField(label='', max_length=200, widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
    }))
    first_name = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Your firstName',
    }))
    last_name = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Your lastName',
    }))
    password = forms.CharField(label='', max_length=200, widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
    }))
    confirm_password = forms.CharField(label='', max_length=200, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_name_field(username, 'username')

        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('This username already exists')
        
        return username
    
    def clean_first_name(self):
        first_name = str(self.cleaned_data.get('first_name'))
        return validate_name_field(first_name, 'firstName')
    
    def clean_last_name(self):
        last_name = str(self.cleaned_data.get('last_name'))
        return validate_name_field(last_name, 'lastName')
    
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords must match')
        
        if len(password) < 8 or len(confirm_password) < 8:
            raise ValidationError('Password must be 8 or longer characters')


class UserSignInForm(forms.Form):
    username = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
    }))
    password = forms.CharField(label='', max_length=200, widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
    }))


class UserEditForm(forms.Form):
    username = forms.CharField(label='', max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
    }))
    email = forms.EmailField(label='', max_length=255, widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
    }))
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Your firstName',
    }))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Your lastName',
    }))
    bio = forms.CharField(label='', max_length=150, required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Your bio',
    }))
    image = forms.ImageField(label='', required=False, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'gif'])], widget=forms.FileInput(attrs={
        'class': 'file-input',
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return validate_name_field(username, 'username')
    
    def clean_first_name(self):
        first_name = str(self.cleaned_data.get('first_name'))
        return validate_name_field(first_name, 'firstName')
    
    def clean_last_name(self):
        last_name = str(self.cleaned_data.get('last_name'))
        return validate_name_field(last_name, 'lastName')