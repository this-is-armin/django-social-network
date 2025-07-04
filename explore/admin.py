from django.contrib import admin
from .models import Post, Comment, PostSave, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_max_show_all = 200
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_filter = ['post', 'user', 'created_at']
    search_fields = ['body']
    readonly_fields = ['created_at']
    list_max_show_all = 200
    list_per_page = 20


@admin.register(PostSave)
class PostSaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_filter = ['post', 'user', 'created_at']
    readonly_fields = ['created_at']
    list_max_show_all = 200
    list_per_page = 20


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_filter = ['post', 'user', 'created_at']
    readonly_fields = ['created_at']
    list_max_show_all = 200
    list_per_page = 20
