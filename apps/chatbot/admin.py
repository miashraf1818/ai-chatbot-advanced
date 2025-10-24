"""
Chatbot Admin Configuration
"""

from django.contrib import admin
from .models import Conversation, Message, ChatbotIntent, ChatbotFeedback


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at', 'is_active', 'get_message_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'user__username']
    date_hierarchy = 'created_at'

    def get_message_count(self, obj):
        return obj.get_message_count()

    get_message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'message_type', 'content_preview', 'intent', 'confidence', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content', 'intent']
    date_hierarchy = 'timestamp'

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'


@admin.register(ChatbotIntent)
class ChatbotIntentAdmin(admin.ModelAdmin):
    list_display = ['tag', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['tag']


@admin.register(ChatbotFeedback)
class ChatbotFeedbackAdmin(admin.ModelAdmin):
    list_display = ['message', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['comment']
    date_hierarchy = 'created_at'
