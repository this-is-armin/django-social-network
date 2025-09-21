from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse
from django.db import models

import os


User = settings.AUTH_USER_MODEL


def generate_user_profile_image_path(instance, filename):
    username = slugify(instance.username)
    filename = f"{username}{os.path.splitext(filename)[1]}"
    file_path = f"accounts/{username}/{filename}"
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if os.path.isfile(full_path):
        os.remove(full_path)
    return file_path


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to=generate_user_profile_image_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_profile_url(self):
        return reverse('accounts:profile', args=[self.username])

    def get_edit_url(self):
        return reverse('accounts:edit_account', args=[self.username])

    def get_delete_profile_image_url(self):
        return reverse('accounts:delete_profile_image', args=[self.username])

    def get_delete_url(self):
        return reverse('accounts:delete_account', args=[self.username])

    def get_follow_url(self):
        return reverse('accounts:follow', args=[self.username])

    def get_unfollow_url(self):
        return reverse('accounts:unfollow', args=[self.username])

    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()

    def get_followers(self):
        return CustomUser.objects.filter(following__to_user=self)

    def get_following(self):
        return CustomUser.objects.filter(followers__from_user=self)

    def get_followers_url(self):
        return reverse('accounts:followers', args=[self.username])

    def get_following_url(self):
        return reverse('accounts:following', args=[self.username])

    def get_create_post_url(self):
        return reverse('accounts:create_post', args=[self.username])
    
    def get_posts_count(self):
        return self.posts.count()
    
    def get_posts_url(self):
        return reverse('accounts:posts', args=[self.username])
    
    def get_notifications_count(self):
        return self.notifications.filter(is_read=False).count()


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.from_user} followed {self.to_user}'
    
    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError('Users can not follow themselves')
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)