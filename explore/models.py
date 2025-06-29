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
    def post_delete(self):
        return reverse('explore:post-delete', args=[self.pk])
    
    @property
    def post_edit(self):
        return reverse('explore:post-edit', args=[self.pk])
    
    @property
    def post_save(self):
        return reverse('explore:post-save', args=[self.pk])
    
    @property
    def post_unsave(self):
        return reverse('explore:post-unsave', args=[self.pk])
    
    @property
    def post_like(self):
        return reverse('explore:post-like', args=[self.pk])
    
    @property
    def post_unlike(self):
        return reverse('explore:post-unlike', args=[self.pk])
    
    @property
    def post_likes_count(self):
        return self.likes.count()
  

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
    def comment_delete(self):
        return reverse('explore:comment-delete', args=[self.pk])


class PostSave(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.post.title


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.post.title