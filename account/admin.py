from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Relation, Music, Image, Profile, Story


class ProfileInline(admin.StackedInline):
    model = Profile

class ExtendedUserAdmin(UserAdmin):
    inlines = [ProfileInline]


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'created']
    list_filter = ['from_user', 'to_user', 'created']


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'singer_name', 'music_name', 'created']
    list_display = ['user', 'singer_name', 'music_name', 'created']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created']
    list_filter = ['id', 'user', 'created']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'created']
	list_filter = ['user', 'created']



admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)