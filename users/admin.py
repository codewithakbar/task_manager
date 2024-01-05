from django.contrib import admin
from .models import CustomUser, Departaments, Notification
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin
from django.contrib.auth.admin import UserAdmin



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username', 'full_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)


@admin.register(Departaments)
class DepartamentsAdmin(DraggableMPTTAdmin):
    list_display = ('title', 'users', 'image')
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title')


