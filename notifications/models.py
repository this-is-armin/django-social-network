from django.db import models
from django.conf import settings
from django.urls import reverse

from accounts.models import Relation
from posts.models import Post, Comment, Like


User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('like', 'Like'),
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    # relations
    relation = models.ForeignKey(Relation, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    like = models.ForeignKey(Like, on_delete=models.CASCADE, blank=True, null=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.from_user} -> {self.to_user} [{self.notification_type}]"
    
    def get_read_url(self):
        return reverse('notifications:read', args=[self.pk])
    
    def get_delete_url(self):
        return reverse('notifications:delete', args=[self.pk])