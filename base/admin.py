from django.contrib import admin

from .models import Post, Comment, Like, PostSave


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'created', 'updated']
    list_filter = ['title', 'user', 'created', 'updated']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created']
    list_filter = ['user', 'post', 'created']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created']
    list_filter = ['user', 'post', 'created']


@admin.register(PostSave)
class PostSaveAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'post', 'created']
	list_filter = ['user', 'post', 'created']