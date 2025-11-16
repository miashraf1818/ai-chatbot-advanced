
🤖 AI-Integrated Chatbot (Django + Gemini API + Google Auth)

⸻

🧠 Overview

A Django-based AI chatbot system integrated with Google Gemini API and Google Authentication (OAuth 2.0).
This backend service enables users to securely log in with Google, manage sessions, and chat with an intelligent Gemini-powered assistant.
It’s built to demonstrate scalable, secure, and production-ready AI integration with modern authentication and API communication.

⸻

⚙️ Features
	•	Google Authentication (OAuth 2.0) – Secure user login using Google accounts
	•	Gemini AI Integration – Uses Google’s Gemini API for real-time, intelligent conversations
	•	Django REST Framework – Provides a clean API layer for frontend or mobile clients
	•	Session Management – Maintains user context between conversations
	•	PostgreSQL Database – Stores user profiles, chat logs, and preferences
	•	Environment Variables (.env) – For secure handling of API keys and credentials
	•	Docker Support – Containerized setup for easy deployment

⸻

🛠️ Tech Stack

Category	Tools
Language	Python
Framework	Django REST Framework
AI / LLM	Google Gemini API
Auth / Security	Google OAuth 2.0, JWT
Database	PostgreSQL
Environment	python-dotenv
Deployment	Docker, Render, AWS EC2
Dev Tools	Git, Postman, VS Code, PyCharm


⸻

📁 Project Structure

ai-chatbot-django/
│
├── manage.py
├── core/
│   ├── settings.py # Environment & Gemini key config
│   ├── urls.py  # API routing
│   └── wsgi.py
│
├── users/
│   ├── models.py  # Google user profiles
│   ├── views.py  # Google login and tokens
│   ├── serializers.py
│   └── urls.py
│
├── chat/
│   ├── views.py  # Chat logic with Gemini API
│   ├── services.py # Gemini API integration functions
│   ├── serializers.py
│   └── urls.py
│
├── requirements.txt # Dependencies
├── Dockerfile # Container setup
└── .env.example # Sample environment variables

⸻

🚀 Getting Started

1️⃣ Clone the repository

git clone https://github.com/miashraf1818/ai-chatbot-advanced.git
cd ai-chatbot-advanced

2️⃣ Create virtual environment and install dependencies

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3️⃣ Setup environment variables

Copy .env.example to .env and add your credentials:

SECRET_KEY=your_django_secret_key
DEBUG=True
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgres_connection_string

4️⃣ Apply migrations

python manage.py migrate

5️⃣ Run the development server

python manage.py runserver

6️⃣ Access the API docs

Open your browser:

http://127.0.0.1:8000/api/docs


⸻

🧩 API Endpoints

Method	Endpoint	Description
POST	/auth/google/	Login via Google OAuth
GET	/chat/	Get chat history
POST	/chat/send/	Send a prompt to Gemini
GET	/health/	API health check

Example Request (POST /chat/send/)

{
  "prompt": "Tell me about Django REST Framework"
}

Example Response

{
  "response": "Django REST Framework is a toolkit for building web APIs in Django..."
}


⸻

🎯 Use Cases
	•	Intelligent chatbot for authenticated users
	•	AI-powered support system with user history
	•	Scalable backend for web or mobile chat interfaces
	•	Example for integrating LLMs securely with OAuth authentication

⸻

🧠 What I Learned
	•	Implementing Google OAuth 2.0 login flow in Django
	•	Integrating Google Gemini API for real-time conversations
	•	Designing token-based authentication with DRF + JWT
	•	Managing environment variables and API security
	•	Structuring modular, maintainable Django applications

⸻

🧑‍💻 Author

Mohammed Ikram Ashrafi
	•	📧 Email: ikramshariff2005@gmail.com
	•	🌐 Portfolio: mohammed-ikram-ashrafi.vercel.app
	•	💼 LinkedIn: linkedin.com/in/mohammed-ikram-ashrafi

⸻

📜 License

This project is licensed under the MIT License.
You’re free to use, modify, and distribute it with proper attribution.

⸻

🌟 Summary

Django-based AI chatbot backend integrating Google Gemini API and Google Authentication, designed for secure, intelligent, and scalable real-time conversations.

