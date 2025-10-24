"""
Chatbot Prediction Engine
Loads trained model and generates responses
"""

import pickle
import random
import nltk
from nltk.stem import WordNetLemmatizer
from pathlib import Path


class ChatbotEngine:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.base_dir = Path(__file__).resolve().parent.parent
        self.model_path = self.base_dir / 'ml_models' / 'trained_models'

        # Load models
        self.load_models()

    def load_models(self):
        """Load trained models and data"""
        try:
            # Load model
            with open(self.model_path / 'chatbot_model.pkl', 'rb') as f:
                self.model = pickle.load(f)

            # Load vectorizer
            with open(self.model_path / 'vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)

            # Load responses
            with open(self.model_path / 'responses.pkl', 'rb') as f:
                self.responses_dict = pickle.load(f)

            print("✓ Models loaded successfully!")

        except Exception as e:
            print(f"Error loading models: {e}")
            raise

    def preprocess_text(self, text):
        """Preprocess and lemmatize text"""
        tokens = nltk.word_tokenize(text.lower())
        lemmatized = [self.lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(lemmatized)

    def predict_intent(self, message):
        """Predict intent from user message"""
        # Preprocess message
        processed_message = self.preprocess_text(message)

        # Vectorize
        message_vector = self.vectorizer.transform([processed_message]).toarray()

        # Predict intent
        intent = self.model.predict(message_vector)[0]

        # Get confidence (probability)
        probabilities = self.model.predict_proba(message_vector)[0]
        confidence = max(probabilities)

        return intent, confidence

    def get_response(self, intent):
        """Get a random response for the predicted intent"""
        if intent in self.responses_dict:
            responses = self.responses_dict[intent]
            return random.choice(responses)
        else:
            return "I'm not sure how to respond to that. Can you rephrase?"

    def chat(self, message):
        """Main chat function - predicts intent and returns response"""
        try:
            # Predict intent
            intent, confidence = self.predict_intent(message)

            # Get response
            response = self.get_response(intent)

            return {
                'message': message,
                'intent': intent,
                'confidence': float(confidence),
                'response': response
            }

        except Exception as e:
            return {
                'message': message,
                'intent': 'error',
                'confidence': 0.0,
                'response': f"Sorry, I encountered an error: {str(e)}"
            }


# Test the chatbot
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("CHATBOT ENGINE TEST")
    print("=" * 50 + "\n")

    # Initialize engine
    engine = ChatbotEngine()

    # Test messages
    test_messages = [
        "Hello!",
        "How are you?",
        "What can you do?",
        "Tell me a joke",
        "Thanks for your help",
        "Goodbye!"
    ]

    print("Testing chatbot responses:\n")
    for msg in test_messages:
        result = engine.chat(msg)
        print(f"User: {msg}")
        print(f"Intent: {result['intent']} (Confidence: {result['confidence']:.2f})")
        print(f"Bot: {result['response']}\n")
