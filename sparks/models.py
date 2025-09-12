from django.db import models
from django.urls import reverse
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Spark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sparks')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.content
    
    def get_absolute_url(self):
        return reverse('sparks:spark_detail', args=[self.pk])
    
    def get_edit_url(self):
        return reverse('sparks:edit_spark', args=[self.pk])
    
    def get_delete_url(self):
        return reverse('sparks:delete_spark', args=[self.pk])

    def get_comments_list(self):
        return self.comments.all()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    spark = models.ForeignKey(Spark, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.body