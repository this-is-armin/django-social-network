from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
from django.db import models

from utils.validators import UsernameValidator, NameValidator
from utils.paths import get_user_image_upload_path


User = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UsernameValidator()],
        help_text='Required. 150 characters or fewer. Lowercase letters, number and _/.',
        error_messages={
            'unique': 'This username already exists.',
        },
    )
    email = models.EmailField(
        unique=True,
        help_text='Required. Must be a valid and unique email address.',
        verbose_name='email address',
        error_messages={
            'unique': 'This email address already exists.',
        },
    )
    first_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters only.',
        validators=[NameValidator('First Name')],
    )
    last_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters only.',
        validators=[NameValidator('Last Name')],
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text='Required. 15 characters or fewer.',
        error_messages={
            'unique': 'This phone number already exists.',
        },
    )
    bio = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to=get_user_image_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])],
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    class Meta:
        ordering = ['username']
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
        return reverse('posts:create_post')
    
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