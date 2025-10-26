from django.urls import path
from apps.chatbot.api.views.chat_views import (
    ChatAPIView,
    ConversationListAPIView,
    ConversationDetailAPIView,
    HealthCheckAPIView,
    SearchConversationsAPIView
)
from apps.chatbot.api.views.admin_views import (
    admin_dashboard_stats,
    admin_users_list,
    admin_user_detail,
    admin_toggle_user_status,
    admin_delete_user,
    admin_system_health
)

app_name = 'chatbot'

urlpatterns = [
    # Health check
    path('health/', HealthCheckAPIView.as_view(), name='health'),

    # Chat endpoints
    path('chat/', ChatAPIView.as_view(), name='chat'),

    # Conversation endpoints
    path('conversations/', ConversationListAPIView.as_view(), name='conversation-list'),
    path('conversations/<int:conversation_id>/', ConversationDetailAPIView.as_view(), name='conversation-detail'),

    # Search endpoint
    path('search/', SearchConversationsAPIView.as_view(), name='search'),

    # ========== ADMIN ROUTES ========== (✅ FIXED - Removed 'api/' prefix)
    path('admin/dashboard/', admin_dashboard_stats, name='admin-dashboard'),
    path('admin/users/', admin_users_list, name='admin-users-list'),
    path('admin/users/<int:user_id>/', admin_user_detail, name='admin-user-detail'),
    path('admin/users/<int:user_id>/toggle/', admin_toggle_user_status, name='admin-toggle-user'),
    path('admin/users/<int:user_id>/delete/', admin_delete_user, name='admin-delete-user'),
    path('admin/health/', admin_system_health, name='admin-health'),
]
