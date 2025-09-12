from django import forms
from .models import Spark, Comment


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


class EditSparkForm(forms.ModelForm):
    class Meta:
        model = Spark
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Edit your spark...',
                'class': 'form-control',
            }),
        }