from django.db import models
from django.conf import settings
from django.urls import reverse


User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (self.body[:20] + '...') if len(self.body) > 20 else self.body

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('accounts:edit_post', args=[self.user.username, self.pk])

    def get_delete_url(self):
        return reverse('accounts:delete_post', args=[self.user.username, self.pk])
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_like_url(self):
        return reverse('posts:like', args=[self.pk])
    
    def get_unlike_url(self):
        return reverse('posts:unlike', args=[self.pk])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return (self.body + '...') if len(self.body) > 20 else self.body


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} liked {self.post}"