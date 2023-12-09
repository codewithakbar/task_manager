from django.contrib import admin
from .models import CustomUser, Departaments, Notification

from mptt.admin import DraggableMPTTAdmin



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)



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


