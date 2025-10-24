"""Admin Dashboard Views"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from apps.chatbot.models import Message, Conversation
from apps.analytics.models import ChatAnalytics


def is_admin(user):
    return user.is_staff or user.is_superuser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_stats(request):
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    total_users = User.objects.count()
    total_messages = Message.objects.count()
    total_conversations = Conversation.objects.count()

    return Response({
        'users': {'total': total_users},
        'messages': {'total': total_messages},
        'conversations': {'total': total_conversations}
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users_list(request):
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    users = User.objects.all()
    return Response({
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'is_active': u.is_active
        } for u in users]
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_user_detail(request, user_id):
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    try:
        user = User.objects.get(id=user_id)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active
            }
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def toggle_ban(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        activate = request.data.get('activate', False)

        if activate:
            user.is_active = True
            user.save()
            return Response({
                'success': True,
                'message': f'User {user.username} has been unbanned'
            })
        else:
            user.is_active = not user.is_active
            user.save()

            status = 'unbanned' if user.is_active else 'banned'
            return Response({
                'success': True,
                'message': f'User {user.username} has been {status}'
            })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'error': 'User not found'
        }, status=404)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


# Alias for backward compatibility
admin_toggle_user_status = toggle_ban


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_user(request, user_id):
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'success': True})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_system_health(request):
    if not is_admin(request.user):
        return Response({'error': 'Admin access required'}, status=403)

    return Response({'status': 'healthy'})
