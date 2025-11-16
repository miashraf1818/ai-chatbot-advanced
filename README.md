```markdown
# AI-Integrated Chatbot (Django + Gemini API + Google OAuth)

A Django-based backend for an authenticated AI chatbot that integrates with Google Gemini (LLM) and Google OAuth 2.0. This repository demonstrates a modular, secure, and production-ready approach to building an authenticated chatbot service using Django REST Framework.

---

## Features

- Google Authentication (OAuth 2.0) — secure user login using Google accounts  
- Google Gemini API integration — real-time AI-driven responses  
- Django REST Framework — API-first backend for web or mobile clients  
- JWT-based session/token management  
- PostgreSQL for user profiles, chat logs, and preferences  
- Environment variables (.env) for secure credential handling  
- Docker support for containerized deployment

---

## Tech Stack

- Language: Python  
- Framework: Django, Django REST Framework  
- AI / LLM: Google Gemini API  
- Auth / Security: Google OAuth 2.0, JWT  
- Database: PostgreSQL  
- Environment management: python-dotenv  
- Deployment: Docker, Render, AWS EC2

---

## Repository layout

ai-chatbot-django/

- manage.py
- core/
  - settings.py        — environment & Gemini key config
  - urls.py            — API routing
  - wsgi.py
- users/
  - models.py          — Google user profiles
  - views.py           — Google login and token handling
  - serializers.py
  - urls.py
- chat/
  - views.py           — chat endpoints and logic
  - services.py        — Gemini API integration functions
  - serializers.py
  - urls.py
- requirements.txt
- Dockerfile
- .env.example
- README.md

---

## Quick start (development)

1. Clone the repository

```bash
git clone https://github.com/miashraf1818/ai-chatbot-advanced.git
cd ai-chatbot-advanced
```

2. Create and activate a virtual environment

macOS / Linux:
```bash
python -m venv venv
source venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Copy and configure environment variables

```bash
cp .env.example .env
# then edit .env and add your credentials
```

Required environment variables (example):
```
SECRET_KEY=your_django_secret_key
DEBUG=True
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgres://user:pass@host:port/dbname
```

5. Apply migrations

```bash
python manage.py migrate
```

6. Run the development server

```bash
python manage.py runserver
```

7. API docs (if available)

Open: http://127.0.0.1:8000/api/docs

---

## Docker (optional)

A Dockerfile is included for containerized runs. Typical workflow:

```bash
docker build -t ai-chatbot-advanced .
docker run -e DATABASE_URL="..." -e GEMINI_API_KEY="..." -p 8000:8000 ai-chatbot-advanced
```

Adjust environment variables and settings for production-level deployment (use an environment secrets manager and HTTPS).

---

## API Endpoints (examples)

- POST /auth/google/ — Login via Google OAuth (exchange code/token, create or fetch user, return JWT)
- GET /chat/ — Get chat history (authenticated)
- POST /chat/send/ — Send a prompt to Gemini and receive an AI response (authenticated)
- GET /health/ — API health check

Example: POST /chat/send/

Request body:
```json
{
  "prompt": "Tell me about Django REST Framework"
}
```

Example response:
```json
{
  "response": "Django REST Framework is a toolkit for building web APIs in Django..."
}
```

Authentication:
- Endpoints under /chat/ require a valid JWT (or session, depending on your configuration).
- /auth/google/ handles the OAuth flow and should return tokens or set cookies depending on your frontend contract.

---

## Security & Production notes

- Never commit secrets (GEMINI_API_KEY, GOOGLE_CLIENT_SECRET, SECRET_KEY).
- Use HTTPS in production and secure JWT cookies or storage.
- Rotate API keys and OAuth credentials periodically.
- Use a managed Postgres service or secure your database (network rules, credentials, backups).
- Consider rate limiting and usage quotas for calls to Gemini to avoid unexpected costs.

---

## Contributing

Contributions are welcome. To contribute:

1. Open an issue describing the bug or enhancement.
2. Fork the repo and create a feature branch.
3. Submit a pull request with tests and a clear description.

---

## Author

Mohammed Ikram Ashrafi  
- Email: ikramshariff2005@gmail.com  
- Portfolio: https://mohammed-ikram-ashrafi.vercel.app  
- LinkedIn: https://linkedin.com/in/mohammed-ikram-ashrafi

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
```
