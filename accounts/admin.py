from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Relation


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    ordering = ['username']
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'image',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'image',)}),
    )


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'created_at']
    list_filter = ['from_user', 'to_user', 'created_at']
    search_fields = ['from_user', 'to_user']
    readonly_fields = ['created_at']
    list_max_show_all = 200
    list_per_page = 20