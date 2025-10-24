"""
Chatbot Service
Business logic for chatbot functionality
"""

from ml_models.chatbot_engine import ChatbotEngine
from apps.chatbot.models import Conversation, Message
from django.contrib.auth.models import User
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class ChatbotService:
    """Service class to handle chatbot logic"""

    def __init__(self):
        """Initialize chatbot engine"""
        try:
            self.engine = ChatbotEngine()
            logger.info("Chatbot engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chatbot engine: {e}")
            self.engine = None

    def get_or_create_conversation(self, user=None):
        """Get existing active conversation or create new one"""
        if user:
            # Get user's active conversation
            conversation = Conversation.objects.filter(
                user=user,
                is_active=True
            ).first()

            if not conversation:
                # Create new conversation
                conversation = Conversation.objects.create(
                    user=user,
                    title=f"Chat - {timezone.now().strftime('%Y-%m-%d %H:%M')}"
                )
        else:
            # Anonymous user - create conversation without user
            conversation = Conversation.objects.create(
                title=f"Anonymous Chat - {timezone.now().strftime('%Y-%m-%d %H:%M')}"
            )

        return conversation

    def process_message(self, user_message, conversation_id=None, user=None):
        """
        Process user message and generate bot response
        HYBRID MODE: Uses ML for simple queries, Gemini AI for complex ones (FREE!)
        """
        try:
            # Get or create conversation
            if conversation_id:
                conversation = Conversation.objects.get(id=conversation_id)
            else:
                conversation = self.get_or_create_conversation(user)

            # Save user message
            user_msg = Message.objects.create(
                conversation=conversation,
                message_type='user',
                content=user_message,
                timestamp=timezone.now()
            )

            # Try ML engine first for simple queries
            ml_result = None
            if self.engine:
                ml_result = self.engine.chat(user_message)

            # Decide which engine to use based on confidence
            use_ai = False

            # Use Gemini AI if:
            # 1. ML confidence is low (< 0.65)
            # 2. Question is longer (more than 5 words)
            # 3. Contains question words that need real information

            question_keywords = ['what', 'when', 'where', 'why', 'how', 'who', 'explain', 'tell me']
            contains_question = any(word in user_message.lower() for word in question_keywords)

            if ml_result:
                if ml_result['confidence'] < 0.65 or len(user_message.split()) > 5:
                    use_ai = True
            else:
                use_ai = True

            # Get response
            if use_ai:
                # Try Gemini AI (FREE!)
                from ml_models.gemini_engine import GeminiEngine
                gemini = GeminiEngine()

                if gemini.is_available():
                    # Get conversation history for context
                    history = conversation.messages.order_by('timestamp')[:10]
                    conv_history = [
                        {
                            'role': 'user' if msg.message_type == 'user' else 'assistant',
                            'content': msg.content
                        }
                        for msg in history
                    ]

                    result = gemini.chat(user_message, conv_history)
                    bot_response = result['response']
                    intent = result['intent']
                    confidence = result['confidence']
                else:
                    # Fallback to ML
                    bot_response = ml_result['response'] if ml_result else "I'm currently unavailable."
                    intent = ml_result['intent'] if ml_result else 'error'
                    confidence = ml_result['confidence'] if ml_result else 0.0
            else:
                # Use ML engine result (fast!)
                bot_response = ml_result['response']
                intent = ml_result['intent']
                confidence = ml_result['confidence']

            # Save bot message
            bot_msg = Message.objects.create(
                conversation=conversation,
                message_type='bot',
                content=bot_response,
                intent=intent,
                confidence=confidence,
                timestamp=timezone.now()
            )

            # Update conversation timestamp
            conversation.updated_at = timezone.now()
            conversation.save()

            return {
                'success': True,
                'conversation_id': conversation.id,
                'user_message': {
                    'id': user_msg.id,
                    'content': user_msg.content,
                    'timestamp': user_msg.timestamp
                },
                'bot_message': {
                    'id': bot_msg.id,
                    'content': bot_msg.content,
                    'intent': bot_msg.intent,
                    'confidence': bot_msg.confidence,
                    'timestamp': bot_msg.timestamp
                }
            }

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_conversation_history(self, conversation_id):
        """Get all messages in a conversation"""
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            messages = conversation.messages.all().order_by('timestamp')

            return {
                'success': True,
                'conversation': {
                    'id': conversation.id,
                    'title': conversation.title,
                    'created_at': conversation.created_at,
                    'updated_at': conversation.updated_at
                },
                'messages': [
                    {
                        'id': msg.id,
                        'type': msg.message_type,
                        'content': msg.content,
                        'intent': msg.intent,
                        'confidence': msg.confidence,
                        'timestamp': msg.timestamp
                    }
                    for msg in messages
                ]
            }
        except Conversation.DoesNotExist:
            return {
                'success': False,
                'error': 'Conversation not found'
            }

    def get_user_conversations(self, user):
        """Get all conversations for a user"""
        conversations = Conversation.objects.filter(
            user=user
        ).order_by('-updated_at')

        return [
            {
                'id': conv.id,
                'title': conv.title,
                'message_count': conv.get_message_count(),
                'created_at': conv.created_at,
                'updated_at': conv.updated_at,
                'is_active': conv.is_active
            }
            for conv in conversations
        ]
