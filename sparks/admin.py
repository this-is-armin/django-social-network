from django.contrib import admin
from .models import Spark, Comment


@admin.register(Spark)
class SparkAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at', 'updated_at']
    search_fields = ['content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'spark', 'created_at']
    list_filter = ['user', 'spark', 'created_at']
    search_fields = ['body']