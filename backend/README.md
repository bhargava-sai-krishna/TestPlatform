
# Flask Auth Service (Exam Platform)

JWT auth with bcrypt hashing and encrypted email-at-rest.

## Setup
```
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```
Create `.env` with:
```
FLASK_SECRET=dev-secret-change-me
JWT_SECRET=dev-jwt-secret-change-me
EMAIL_ENC_KEY=PUT_FERNET_KEY_HERE   # Generate: python - <<<'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
DATABASE_URL=sqlite:///dev.db       # or postgres/mysql URL
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Run
```
python app.py
```

## Endpoints
- POST /api/auth/register  {email, password, full_name?}
- POST /api/auth/login     {email, password}
- GET  /api/auth/me        (Bearer access token)
- POST /api/auth/refresh   (Bearer refresh token)
