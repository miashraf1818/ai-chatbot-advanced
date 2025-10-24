"""
Google Gemini API Integration
Uses Gemini AI for advanced responses (FREE!)
"""

import google.generativeai as genai
from decouple import config
import logging

logger = logging.getLogger(__name__)


class GeminiEngine:
    """
    Google Gemini AI Integration
    FREE API for intelligent chatbot responses
    """

    def __init__(self):
        """Initialize Gemini client"""
        api_key = config('GEMINI_API_KEY', default=None)

        if not api_key:
            logger.warning("Gemini API key not found")
            self.model = None
            return

        try:
            genai.configure(api_key=api_key)

            # Use Gemini Pro (free tier)
            self.model = genai.GenerativeModel(
                'gemini-2.0-flash',
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_output_tokens': 500,
                }
            )

            # Start chat session
            self.chat_session = None

            logger.info("Gemini engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self.model = None

    def is_available(self):
        """Check if Gemini is available"""
        return self.model is not None

    def chat(self, message, conversation_history=None):
        """
        Send message to Gemini and get response

        Args:
            message: User message
            conversation_history: List of previous messages (optional)

        Returns:
            dict with response, intent, and confidence
        """
        if not self.is_available():
            return {
                'response': "Gemini API is not configured.",
                'intent': 'error',
                'confidence': 0.0
            }

        try:
            # Create system prompt
            system_prompt = """You are a helpful, friendly AI assistant in a chat application. 
Your responses should be:
- Clear and concise (2-3 sentences max)
- Friendly and conversational
- Helpful and informative
- Natural and engaging

Keep responses short and to the point."""

            # Build conversation context
            if conversation_history and len(conversation_history) > 0:
                # Start new chat with history
                history = []
                for msg in conversation_history[-5:]:  # Last 5 messages
                    if msg['role'] == 'user':
                        history.append({
                            'role': 'user',
                            'parts': [msg['content']]
                        })
                    elif msg['role'] == 'assistant':
                        history.append({
                            'role': 'model',
                            'parts': [msg['content']]
                        })

                self.chat_session = self.model.start_chat(history=history)
                response = self.chat_session.send_message(message)
            else:
                # Single message
                full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
                response = self.model.generate_content(full_prompt)

            # Extract response text
            bot_response = response.text

            return {
                'response': bot_response,
                'intent': 'gemini',
                'confidence': 0.95
            }

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return {
                'response': f"Sorry, I encountered an error: {str(e)}",
                'intent': 'error',
                'confidence': 0.0
            }


# Test the engine
if __name__ == "__main__":
    print("\n" + "="*60)
    print("GOOGLE GEMINI ENGINE TEST")
    print("="*60 + "\n")

    engine = GeminiEngine()

    if engine.is_available():
        print("✓ Gemini engine initialized!\n")

        test_messages = [
            "Hello! How are you?",
            "What is Python programming?",
            "Tell me a joke about programmers",
            "What's the capital of France?",
        ]

        for msg in test_messages:
            print(f"User: {msg}")
            result = engine.chat(msg)
            print(f"Bot: {result['response']}")
            print(f"Intent: {result['intent']} | Confidence: {result['confidence']}\n")
            print("-" * 60 + "\n")
    else:
        print("✗ Gemini engine not available. Check API key in .env file.")
