"""
User Models
Extended user profile for chatbot users
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile with additional information
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    notification_enabled = models.BooleanField(default=True)
    theme = models.CharField(
        max_length=10,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )

    # Stats
    total_conversations = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ✅ CREATE PROFILE WHEN USER IS CREATED
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserProfile when User is created
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)


# ✅ SAVE PROFILE WHEN USER IS SAVED
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """
    Save UserProfile when User is saved
    """
    if created:
        # Ensure profile exists for new users
        UserProfile.objects.get_or_create(user=instance)
    else:
        # Save profile only if it exists
        try:
            if hasattr(instance, 'profile'):
                instance.profile.save()
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist
            UserProfile.objects.create(user=instance)
