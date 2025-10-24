"""
Admin Dashboard Views
Handles all admin-related API endpoints
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from apps.chatbot.models import Message, Conversation
from apps.analytics.models import ChatAnalytics


# Admin permission check
def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_stats(request):
    """Get overall system statistics"""
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    # Time ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # User stats
    total_users = User.objects.count()
    active_users_today = User.objects.filter(last_login__date=today).count()
    new_users_week = User.objects.filter(date_joined__gte=week_ago).count()

    # Message stats
    total_messages = Message.objects.count()
    messages_today = Message.objects.filter(timestamp__date=today).count()
    messages_week = Message.objects.filter(timestamp__gte=week_ago).count()

    # Conversation stats
    total_conversations = Conversation.objects.count()
    active_conversations = Conversation.objects.filter(updated_at__gte=week_ago).count()

    return Response({
        'users': {
            'total': total_users,
            'active_today': active_users_today,
            'new_this_week': new_users_week,
        },
        'messages': {
            'total': total_messages,
            'today': messages_today,
            'this_week': messages_week,
        },
        'conversations': {
            'total': total_conversations,
            'active': active_conversations,
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users_list(request):
    """Get list of all users with stats"""
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    users = User.objects.all().annotate(
        message_count=Count('conversation__message', distinct=True),
        conversation_count=Count('conversation', distinct=True)
    ).order_by('-date_joined')

    user_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'is_active': user.is_active,
        'message_count': user.message_count,
        'conversation_count': user.conversation_count,
    } for user in users]

    return Response({'count': len(user_data), 'users': user_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_user_detail(request, user_id):
    """Get detailed info about a specific user"""
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    conversations = Conversation.objects.filter(user=user).order_by('-updated_at')
    total_messages = Message.objects.filter(conversation__user=user).count()

    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined,
            'is_active': user.is_active,
        },
        'stats': {
            'total_messages': total_messages,
            'conversations': conversations.count(),
        },
        'conversations': [{
            'id': conv.id,
            'title': conv.title,
            'created_at': conv.created_at,
        } for conv in conversations[:10]]
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_toggle_user_status(request, user_id):
    """Ban/Unban a user"""
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if user.id == request.user.id:
        return Response({'error': 'Cannot ban yourself'}, status=400)

    user.is_active = not user.is_active
    user.save()

    return Response({
        'success': True,
        'is_active': user.is_active,
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_user(request, user_id):
    """Delete a user"""
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if user.id == request.user.id:
        return Response({'error': 'Cannot delete yourself'}, status=400)

    username = user.username
    user.delete()

    return Response({'success': True, 'message': f'User {username} deleted'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_system_health(request):
    """Get system health metrics"""
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    return Response({
        'database': {
            'users': User.objects.count(),
            'conversations': Conversation.objects.count(),
            'messages': Message.objects.count(),
        },
        'status': 'healthy',
    })
