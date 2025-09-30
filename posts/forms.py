from django import forms
from .models import Comment, Post


class PostCreateEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Write your post...',
                'class': 'form-control',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Write your comment...',
                'class': 'form-control',
            }),
        }