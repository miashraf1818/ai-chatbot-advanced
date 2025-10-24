"""
Chat API Views
"""
from apps.analytics.utils import log_activity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.chatbot.services.chatbot_service import ChatbotService
from apps.chatbot.api.serializers.chat_serializers import (
    ChatRequestSerializer,
    ChatResponseSerializer,
    ConversationSerializer,
    ConversationDetailSerializer
)
from apps.chatbot.models import Conversation, Message
import logging

logger = logging.getLogger(__name__)


class ChatAPIView(APIView):
    """
    Main chat endpoint
    POST: Send message and get bot response
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chatbot_service = ChatbotService()

    def post(self, request):
        """Handle chat message"""
        serializer = ChatRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = serializer.validated_data['message']
        conversation_id = serializer.validated_data.get('conversation_id')

        # Get user if authenticated
        user = request.user if request.user.is_authenticated else None

        # Process message
        result = self.chatbot_service.process_message(
            user_message=message,
            conversation_id=conversation_id,
            user=user
        )

        # ✨ NEW: Log user activity
        if result['success'] and user:
            try:
                log_activity(user, 'message_sent', {
                    'conversation_id': str(result.get('conversation_id')),
                    'message_length': len(message),
                    'has_response': True
                })
            except Exception as e:
                logger.error(f"Error logging activity: {e}")

        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': result.get('error', 'Unknown error')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConversationListAPIView(APIView):
    """
    GET: List all conversations for authenticated user
    """

    def get(self, request):
        """Get user's conversations"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        conversations = Conversation.objects.filter(
            user=request.user
        ).order_by('-updated_at')

        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConversationDetailAPIView(APIView):
    """
    GET: Get conversation details with all messages
    DELETE: Delete conversation
    """

    def get(self, request, conversation_id):
        """Get conversation history"""
        try:
            conversation = Conversation.objects.get(id=conversation_id)

            # Check if user owns conversation (if authenticated)
            if request.user.is_authenticated and conversation.user:
                if conversation.user != request.user:
                    return Response(
                        {'error': 'Permission denied'},
                        status=status.HTTP_403_FORBIDDEN
                    )

            serializer = ConversationDetailSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, conversation_id):
        """Delete conversation"""
        try:
            conversation = Conversation.objects.get(id=conversation_id)

            # Check if user owns conversation
            if request.user.is_authenticated and conversation.user:
                if conversation.user != request.user:
                    return Response(
                        {'error': 'Permission denied'},
                        status=status.HTTP_403_FORBIDDEN
                    )

            conversation.delete()
            return Response(
                {'message': 'Conversation deleted successfully'},
                status=status.HTTP_200_OK
            )

        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class HealthCheckAPIView(APIView):
    """
    Simple health check endpoint
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """Health check"""
        return Response({
            'status': 'healthy',
            'service': 'AI Chatbot API',
            'version': '1.0.0'
        }, status=status.HTTP_200_OK)


class SearchConversationsAPIView(APIView):
    """Search conversations by keyword"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Search user's conversations"""
        query = request.GET.get('q', '').strip()

        if not query:
            return Response({
                'success': False,
                'message': 'Search query required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Search in messages
        messages = Message.objects.filter(
            conversation__user=request.user,
            content__icontains=query
        ).select_related('conversation').order_by('-timestamp')[:50]

        # Get unique conversations
        conversations = {}
        for msg in messages:
            conv = msg.conversation
            if conv.id not in conversations:
                conversations[conv.id] = {
                    'id': conv.id,
                    'title': conv.title,
                    'created_at': conv.created_at.isoformat(),
                    'message_count': conv.messages.count(),
                    'matched_message': msg.content[:100]
                }

        return Response({
            'success': True,
            'results': list(conversations.values()),
            'count': len(conversations)
        })
