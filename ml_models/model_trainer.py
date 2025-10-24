"""
ML Model Trainer
Trains the chatbot model using intents data
"""

import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
from pathlib import Path


class ChatbotTrainer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

        # Get paths
        self.base_dir = Path(__file__).resolve().parent.parent
        self.training_data_path = self.base_dir / 'ml_models' / 'training_data' / 'intents.json'
        self.model_path = self.base_dir / 'ml_models' / 'trained_models'

    def load_intents(self):
        """Load intents from JSON file"""
        print(f"Loading intents from: {self.training_data_path}")

        with open(self.training_data_path, 'r') as file:
            data = json.load(file)

        return data['intents']

    def preprocess_text(self, text):
        """Preprocess and lemmatize text"""
        tokens = nltk.word_tokenize(text.lower())
        lemmatized = [self.lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(lemmatized)

    def prepare_training_data(self, intents):
        """Prepare training data from intents"""
        corpus = []
        labels = []
        self.responses_dict = {}

        print("Preparing training data...")

        for intent in intents:
            tag = intent['tag']

            # Store responses for each tag
            self.responses_dict[tag] = intent['responses']

            # Process each pattern
            for pattern in intent['patterns']:
                processed_pattern = self.preprocess_text(pattern)
                corpus.append(processed_pattern)
                labels.append(tag)

        print(f"Total patterns: {len(corpus)}")
        print(f"Unique intents: {len(set(labels))}")

        return corpus, labels

    def train_model(self):
        """Train the chatbot model"""
        print("\n" + "=" * 50)
        print("TRAINING CHATBOT MODEL")
        print("=" * 50 + "\n")

        # Load and prepare data
        intents = self.load_intents()
        corpus, labels = self.prepare_training_data(intents)

        # Vectorize text
        print("Vectorizing text data...")
        X = self.vectorizer.fit_transform(corpus).toarray()
        y = np.array(labels)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print(f"Training set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")

        # Train model
        print("\nTraining Random Forest model...")
        self.model.fit(X_train, y_train)

        # Evaluate
        print("\nEvaluating model...")
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\n{'=' * 50}")
        print(f"MODEL ACCURACY: {accuracy * 100:.2f}%")
        print(f"{'=' * 50}\n")

        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Save models
        self.save_models()

        return accuracy

    def save_models(self):
        """Save trained models and data"""
        print("\nSaving trained models...")

        # Create directory if it doesn't exist
        self.model_path.mkdir(parents=True, exist_ok=True)

        # Save model
        model_file = self.model_path / 'chatbot_model.pkl'
        with open(model_file, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✓ Model saved: {model_file}")

        # Save vectorizer
        vectorizer_file = self.model_path / 'vectorizer.pkl'
        with open(vectorizer_file, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"✓ Vectorizer saved: {vectorizer_file}")

        # Save responses
        responses_file = self.model_path / 'responses.pkl'
        with open(responses_file, 'wb') as f:
            pickle.dump(self.responses_dict, f)
        print(f"✓ Responses saved: {responses_file}")

        print("\n✓ All models saved successfully!")


if __name__ == "__main__":
    trainer = ChatbotTrainer()
    accuracy = trainer.train_model()
    print(f"\n🎉 Training complete! Final accuracy: {accuracy * 100:.2f}%")
