from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age', 'bio', 'location', 'image',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


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
        user = CustomUser.objects.filter(username=username)

        invalid_chars = ['(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', ',', '~', '`', '!', '?', '@', '#', '$', '%', '^', '&', '*', '-', '+', '=', ' ']
        invalid_names = ['admin', 'ADMIN']
        
        for char in invalid_chars:
            if char in username:
                raise ValidationError('Your username was contain incorrect character(s)')

        for name in invalid_names:
            if name == username:
                raise ValidationError(f"Your username can't be '{name}'")
            
            if name in username:
                raise ValidationError(f"Your username can't contain '{name}'")

        if user.exists():
            raise ValidationError('This username already exists')
        
        return username
    
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
    age = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={
        'placeholder': 'Your age',
    }))
    bio = forms.CharField(label='', max_length=150, required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Your bio',
    }))
    location = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your location',
    }))
    image = forms.ImageField(label='', required=False, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    

    def clean_username(self):
        username = self.cleaned_data.get('username')

        invalid_chars = ['(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', ',', '~', '`', '!', '?', '@', '#', '$', '%', '^', '&', '*', '-', '+', '=', ' ']
        invalid_names = ['admin', 'ADMIN']
        
        for char in invalid_chars:
            if char in username:
                raise ValidationError('Your username was contain incorrect character(s)')

        for name in invalid_names:
            if name == username:
                raise ValidationError(f"Your username can't be '{name}'")
            
            if name in username:
                raise ValidationError(f"Your username can't contain '{name}'")
            
        return username
    
    def clean(self):
        first_name = str(self.cleaned_data.get('first_name'))
        last_name = str(self.cleaned_data.get('last_name'))

        invalid_chars = ['(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', ',', '~', '`', '!', '?', '@', '#', '$', '%', '^', '&', '*', '-', '+', '=', ' ']
        invalid_names = ['admin', 'ADMIN']
        
        # To validate first-name
        for char in invalid_chars:
            if char in first_name:
                raise ValidationError('Your firstName was contain incorrect character(s) or space')

        for name in invalid_names:
            if name == first_name:
                raise ValidationError(f"Your firstName can't be '{name}'")
            
            if name in first_name:
                raise ValidationError(f"Your firstName can't contain '{name}'")
        
        # To validate last-name
        for char in invalid_chars:
            if char in last_name:
                raise ValidationError('Your lastName was contain incorrect character(s) or space')

        for name in invalid_names:
            if name == last_name:
                raise ValidationError(f"Your lastName can't be '{name}'")
            
            if name in last_name:
                raise ValidationError(f"Your lastName can't contain '{name}'")