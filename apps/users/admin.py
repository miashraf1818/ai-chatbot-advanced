"""
Users Admin Configuration
"""

from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'preferred_language', 'total_conversations', 'total_messages', 'created_at']
    list_filter = ['preferred_language', 'theme', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['total_conversations', 'total_messages']
