"""
Views package
"""

# Import chat views
# from .chat_views import *

# Import admin views
from .admin_views import (
    admin_dashboard_stats,
    admin_users_list,
    admin_user_detail,
    admin_toggle_user_status,
    admin_delete_user,
    admin_system_health
)

__all__ = [
    'admin_dashboard_stats',
    'admin_users_list',
    'admin_user_detail',
    'admin_toggle_user_status',
    'admin_delete_user',
    'admin_system_health',
]
