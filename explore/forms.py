from django import forms
from ckeditor.fields import RichTextFormField

from .models import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Post title',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Post description',
            }),
            'body': RichTextFormField(),
        }
        labels = {
            'title': '',
            'description': '',
            'body': '',
        }