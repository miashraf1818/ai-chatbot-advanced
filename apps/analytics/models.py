from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.chatbot.models import Message


class MessageFeedback(models.Model):
    """Store user feedback on bot messages"""
    FEEDBACK_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analytics_message_feedback'
        verbose_name = 'Message Feedback'
        verbose_name_plural = 'Message Feedbacks'
        unique_together = ['user', 'message']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.feedback_type}"


class ChatAnalytics(models.Model):
    """Daily aggregate statistics"""
    date = models.DateField(unique=True, default=timezone.now)
    total_messages = models.IntegerField(default=0)
    total_conversations = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    avg_messages_per_conversation = models.FloatField(default=0.0)
    avg_conversation_duration = models.FloatField(default=0.0)  # in minutes

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chat Analytics'
        verbose_name_plural = 'Chat Analytics'
        ordering = ['-date']

    def __str__(self):
        return f"Analytics for {self.date}"


class IntentAnalytics(models.Model):
    """Track intent usage and accuracy"""
    intent_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    usage_count = models.IntegerField(default=0)
    avg_confidence = models.FloatField(default=0.0)
    successful_responses = models.IntegerField(default=0)
    failed_responses = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Intent Analytics'
        verbose_name_plural = 'Intent Analytics'
        ordering = ['-date', '-usage_count']
        unique_together = ['intent_name', 'date']

    def __str__(self):
        return f"{self.intent_name} - {self.date}"


class UserActivity(models.Model):
    """Track individual user activities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('message_sent', 'Message Sent'),
        ('conversation_started', 'Conversation Started'),
        ('conversation_ended', 'Conversation Ended'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)  # Additional data

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"


class MessageFeedback(models.Model):
    """Store user feedback on bot messages"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey('chatbot.Message', on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    ])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message Feedback'
        verbose_name_plural = 'Message Feedbacks'
        unique_together = ['user', 'message']

    def __str__(self):
        return f"{self.user.username} - {self.feedback_type} - {self.message.id}"
