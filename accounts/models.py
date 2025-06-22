from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=150, null=True, blank=True)
    # image = models.ImageField(upload_to='accounts/images/', null=True, blank=True)

    @property
    def delete_account(self):
        return reverse('accounts:delete-account', args=[self.username])
    
    @property
    def signout_account(self):
        return reverse('accounts:signout')
    
    @property
    def edit_account(self):
        return reverse('accounts:edit-account', args=[self.username])
    
    @property
    def follow_account(self):
        return reverse('accounts:follow', args=[self.username])
    
    @property
    def unfollow_account(self):
        return reverse('accounts:unfollow', args=[self.username])
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    @property
    def followers_page(self):
        return reverse('accounts:followers', args=[self.username])
    
    @property
    def following_page(self):
        return reverse('accounts:following', args=[self.username])
    
    property
    def posts_count(self):
        return self.posts.count()
    
    property
    def posts_page(self):
        return reverse('accounts:posts', args=[self.username])

    property
    def comments_count(self):
        return self.comments.count()
    
    property
    def comments_page(self):
        return reverse('accounts:comments', args=[self.username])
    
    property
    def new_post(self):
        return reverse('explore:new-post')


class Relation(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.from_user} followed {self.to_user}"
    