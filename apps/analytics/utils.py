from apps.analytics.models import UserActivity
from django.utils import timezone

def log_activity(user, activity_type, details=None):
    """Log user activity"""
    try:
        UserActivity.objects.create(
            user=user,
            activity_type=activity_type,
            details=details or {},
            timestamp=timezone.now()
        )
    except Exception as e:
        print(f"Error logging activity: {e}")
