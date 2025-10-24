from django.contrib import admin
from apps.analytics.models import ChatAnalytics, IntentAnalytics, UserActivity, MessageFeedback



@admin.register(ChatAnalytics)
class ChatAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_messages', 'total_conversations', 'active_users']
    list_filter = ['date']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-date']


@admin.register(IntentAnalytics)
class IntentAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['intent_name', 'date', 'usage_count', 'avg_confidence']
    list_filter = ['date', 'intent_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-date', '-usage_count']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    readonly_fields = ['timestamp']
    search_fields = ['user__username']
    ordering = ['-timestamp']

@admin.register(MessageFeedback)
class MessageFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'feedback_type', 'message', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['user__username', 'comment']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    def message_preview(self, obj):
        return obj.message.content[:50] + '...' if len(obj.message.content) > 50 else obj.message.content

    message_preview.short_description = 'Message'