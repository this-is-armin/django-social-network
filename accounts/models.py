from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.conf import settings

import os


def user_profile_image_path(instance, filename):
    profile_picture_path = f"accounts/images/{instance.username}/{filename}"
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_path)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_path


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(
        upload_to=user_profile_image_path, 
        null=True, 
        blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'gif'])]
    )

    # URL Properties
    @property
    def get_profile_url(self):
        return reverse('accounts:profile', args=[self.username])

    @property
    def get_delete_url(self):
        return reverse('accounts:delete-account', args=[self.username])
    
    @property
    def get_signout_url(self):
        return reverse('accounts:signout')
    
    @property
    def get_edit_url(self):
        return reverse('accounts:edit-account', args=[self.username])
    
    @property
    def get_follow_url(self):
        return reverse('accounts:follow', args=[self.username])
    
    @property
    def get_unfollow_url(self):
        return reverse('accounts:unfollow', args=[self.username])
    
    # Count Properties
    @property
    def get_followers_count(self):
        return self.followers.count()
    
    @property
    def get_following_count(self):
        return self.following.count()
    
    @property
    def get_posts_count(self):
        return self.posts.count()
    
    @property
    def get_comments_count(self):
        return self.comments.count()
    
    @property
    def get_saved_posts_count(self):
        return self.saved_posts.count()
    
    @property
    def get_liked_posts_count(self):
        return self.liked_posts.count()
    
    # List URL Properties
    @property
    def get_followers_list_url(self):
        return reverse('accounts:followers', args=[self.username])
    
    @property
    def get_following_list_url(self):
        return reverse('accounts:following', args=[self.username])
    
    @property
    def get_posts_list_url(self):
        return reverse('accounts:posts', args=[self.username])
    
    @property
    def get_saved_posts_list_url(self):
        return reverse('accounts:saved-posts', args=[self.username])
    
    @property
    def get_liked_posts_list_url(self):
        return reverse('accounts:liked-posts', args=[self.username])
    
    @property
    def get_comments_list_url(self):
        return reverse('accounts:comments', args=[self.username])

    # List Properties
    @property
    def get_followers_list(self):
        return self.followers.all()
    
    @property
    def get_following_list(self):
        return self.following.all()
    
    @property
    def get_posts_list(self):
        return self.posts.all()
    
    @property
    def get_saved_posts_list(self):
        return self.saved_posts.all()
    
    @property
    def get_liked_posts_list(self):
        return self.liked_posts.all()
    
    @property
    def get_comments_list(self):
        return self.comments.all()

    # Action URLs
    @property
    def get_new_post_url(self):
        return reverse('explore:new-post')


class Relation(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.from_user} followed {self.to_user}"
    