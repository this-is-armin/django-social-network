from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

from accounts.models import CustomUser


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def get_absolute_url(self):
        return reverse('explore:post', args=[self.pk])
    
    @property
    def delete_post(self):
        return reverse('explore:delete-post', args=[self.pk])
    
    @property
    def edit_post(self):
        return reverse('explore:edit-post', args=[self.pk])
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.body
    
    @property
    def delete_comment(self):
        return reverse('explore:delete-comment', args=[self.pk])