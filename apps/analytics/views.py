from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Avg, Q
from django.db.models.functions import ExtractHour  # Add this import
from datetime import timedelta
from apps.chatbot.models import Conversation, Message
from apps.analytics.models import ChatAnalytics, IntentAnalytics, UserActivity
from apps.analytics.models import MessageFeedback
from apps.chatbot.models import Message
from rest_framework import status
from apps.analytics.models import MessageFeedback
from apps.chatbot.models import Message


class MessageFeedbackView(APIView):
    """Store user feedback on messages"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            message_id = request.data.get('message_id')
            feedback_type = request.data.get('feedback_type')
            comment = request.data.get('comment', '')

            # Validate
            if not message_id or not feedback_type:
                return Response({
                    'success': False,
                    'message': 'Missing required fields'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get message
            message = Message.objects.get(id=message_id)

            # Create or update feedback
            feedback, created = MessageFeedback.objects.update_or_create(
                user=request.user,
                message=message,
                defaults={
                    'feedback_type': feedback_type,
                    'comment': comment
                }
            )

            action = 'created' if created else 'updated'

            return Response({
                'success': True,
                'message': f'Feedback {action} successfully',
                'feedback_id': feedback.id
            })

        except Message.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Message not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DashboardStatsView(APIView):
    """Real-time dashboard statistics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        week_ago = today - timedelta(days=7)

        # Today's stats
        today_messages = Message.objects.filter(timestamp__date=today).count()
        today_conversations = Conversation.objects.filter(created_at__date=today).count()
        today_active_users = Conversation.objects.filter(
            updated_at__date=today
        ).values('user').distinct().count()

        # Yesterday's stats for comparison
        yesterday_messages = Message.objects.filter(timestamp__date=yesterday).count()
        yesterday_conversations = Conversation.objects.filter(created_at__date=yesterday).count()

        # Overall stats
        total_users = User.objects.count()
        total_conversations = Conversation.objects.count()
        total_messages = Message.objects.count()

        # Calculate percentage changes
        message_change = self._calculate_change(today_messages, yesterday_messages)
        conversation_change = self._calculate_change(today_conversations, yesterday_conversations)

        # Average conversation length
        avg_messages = Message.objects.filter(
            timestamp__gte=week_ago
        ).values('conversation').annotate(
            msg_count=Count('id')
        ).aggregate(avg=Avg('msg_count'))['avg'] or 0

        # Most active time (hour of day) - FIXED for SQLite
        popular_hours = Message.objects.filter(
            timestamp__date=today
        ).annotate(
            hour=ExtractHour('timestamp')
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('-count')[:3]

        # Top intents today
        top_intents = Message.objects.filter(
            timestamp__date=today,
            message_type='bot'
        ).exclude(
            intent__isnull=True
        ).values('intent').annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        return Response({
            'success': True,
            'stats': {
                'today': {
                    'messages': today_messages,
                    'conversations': today_conversations,
                    'active_users': today_active_users,
                    'message_change': message_change,
                    'conversation_change': conversation_change,
                },
                'overall': {
                    'total_users': total_users,
                    'total_conversations': total_conversations,
                    'total_messages': total_messages,
                    'avg_conversation_length': round(avg_messages, 1),
                },
                'trends': {
                    'popular_hours': list(popular_hours),
                    'top_intents': list(top_intents),
                }
            }
        })

    def _calculate_change(self, today_val, yesterday_val):
        """Calculate percentage change"""
        if yesterday_val == 0:
            return 100 if today_val > 0 else 0
        return round(((today_val - yesterday_val) / yesterday_val) * 100, 1)


class WeeklyChartDataView(APIView):
    """Data for charts - last 7 days"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # Get daily message counts for last 7 days
        daily_data = []
        for i in range(7):
            date = today - timedelta(days=6 - i)
            messages = Message.objects.filter(timestamp__date=date).count()
            conversations = Conversation.objects.filter(created_at__date=date).count()

            daily_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': date.strftime('%a'),  # Mon, Tue, etc.
                'messages': messages,
                'conversations': conversations,
            })

        return Response({
            'success': True,
            'chart_data': daily_data
        })


class IntentAnalyticsView(APIView):
    """Intent usage statistics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # Get intent statistics
        intent_stats = Message.objects.filter(
            timestamp__date=today,
            message_type='bot'
        ).exclude(
            intent__isnull=True
        ).values('intent').annotate(
            count=Count('id'),
            avg_confidence=Avg('confidence')
        ).order_by('-count')

        return Response({
            'success': True,
            'intents': list(intent_stats)
        })


class MessageFeedbackView(APIView):
    """Store and retrieve message feedback"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            message_id = request.data.get('message_id')
            feedback_type = request.data.get('feedback_type')
            comment = request.data.get('comment', '')

            message = Message.objects.get(id=message_id)

            # Create or update feedback
            feedback, created = MessageFeedback.objects.update_or_create(
                user=request.user,
                message=message,
                defaults={
                    'feedback_type': feedback_type,
                    'comment': comment
                }
            )

            return Response({
                'success': True,
                'message': 'Feedback saved successfully',
                'feedback_id': feedback.id
            })

        except Message.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Message not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)