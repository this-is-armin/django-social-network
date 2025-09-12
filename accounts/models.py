from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse

import os


User = settings.AUTH_USER_MODEL


def generate_user_image_path(instance, filename):
    username = slugify(instance.username)
    filename = f'{username}{os.path.splitext(filename)[1]}'
    file_path = f'accounts/{username}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if os.path.isfile(full_path):
        os.remove(full_path)
    return file_path


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=generate_user_image_path,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_profile_url(self):
        return reverse('accounts:profile', args=[self.username])
    
    def get_edit_account_url(self):
        return reverse('accounts:edit_account', args=[self.username])
    
    def get_delete_profile_image_url(self):
        return reverse('accounts:delete_profile_image', args=[self.username])
    
    def get_delete_account_url(self):
        return reverse('accounts:delete_account', args=[self.username])
     
    def get_add_spark_url(self):
        return reverse('accounts:add_spark', args=[self.username])
    
    def get_sparks_count(self):
        return self.sparks.count()
    
    def get_sparks_list(self):
        return self.sparks.all()
    
    def get_sparks_list_url(self):
        return reverse('accounts:sparks', args=[self.username])
    
    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()
    
    def get_followers_list(self):
        return CustomUser.objects.filter(followers__to_user=self)
    
    def get_following_list(self):
        return CustomUser.objects.filter(followers__from_user=self)
    
    def get_followers_list_url(self):
        return reverse('accounts:followers_list', args=[self.username])
    
    def get_following_list_url(self):
        return reverse('accounts:following_list', args=[self.username])
    
    def get_follow_url(self):
        return reverse('accounts:follow', args=[self.username])
    
    def get_unfollow_url(self):
        return reverse('accounts:unfollow', args=[self.username])


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