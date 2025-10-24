"""
Chatbot Models
Defines the database structure for chat conversations and messages
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversation(models.Model):
    """
    Represents a chat conversation/session
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200, default='New Conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def get_message_count(self):
        """Return total messages in this conversation"""
        return self.messages.count()


class Message(models.Model):
    """
    Represents individual messages in a conversation
    """
    MESSAGE_TYPE_CHOICES = [
        ('user', 'User Message'),
        ('bot', 'Bot Response'),
        ('system', 'System Message'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        default='user'
    )
    content = models.TextField()
    intent = models.CharField(max_length=100, blank=True, null=True)
    confidence = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(default=timezone.now)

    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}"


class ChatbotIntent(models.Model):
    """
    Stores chatbot intents/patterns for training
    """
    tag = models.CharField(max_length=100, unique=True)
    patterns = models.JSONField(default=list)  # List of example phrases
    responses = models.JSONField(default=list)  # List of possible responses
    context_set = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tag']
        verbose_name = 'Chatbot Intent'
        verbose_name_plural = 'Chatbot Intents'

    def __str__(self):
        return self.tag


class ChatbotFeedback(models.Model):
    """
    Stores user feedback on bot responses for improvement
    """
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chatbot Feedback'
        verbose_name_plural = 'Chatbot Feedback'

    def __str__(self):
        return f"Feedback: {self.rating} stars"
