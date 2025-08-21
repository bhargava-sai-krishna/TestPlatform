# 📝 LeadMasters AI — Exam & Auth System

This is my submission for the **LeadMasters AI Challenge**.
The project implements a **user authentication system** with **exam functionality**, profile management, and secure backend APIs.

---

## ⚙️ Tech Stack

* 🔙 **Backend**: Python (Flask, Flask-CORS, Flask-SQLAlchemy, Flask-JWT-Extended, Flasgger for docs)
* ⚛️ **Frontend**: React.js
* 🛢 **Database**: PostgreSQL (via SQLAlchemy ORM)
* 🧪 **Testing**: Postman / API collection

---

## 📂 Project Structure

```
LeadMasters_AI/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── exam.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   ├── security.py
│   ├── app.py
│   ├── .env
│   ├── requirements.txt
│   ├── postman_collection.json
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Profile.js
│   │   │   └── Exam.js
│   │   ├── utils/api.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── App.css
│   ├── package.json
│
└── README.md
```

---

## 🧪 How to Run

### 🔧 Backend (Flask + PostgreSQL)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # On Windows
pip install -r requirements.txt

# Ensure PostgreSQL is running & DATABASE_URL is set in .env
flask db upgrade  # Run migrations

# Start server
python app.py
```

Server runs at: **[http://127.0.0.1:8001](http://127.0.0.1:8001)**

---

### ⚛️ Frontend (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs at: **[http://localhost:3000](http://localhost:3000)**

---

## ✅ Completed Features

### ✔️ Authentication

* User registration with secure password hashing
* JWT-based login & token refresh
* Profile endpoint with protected access

### ✔️ Exam System

* Start new exam session
* Auto-randomized 10 questions
* Answer submission with scoring
* Prevents resubmission once submitted
* Exam timer (30 mins)

### ✔️ UI/UX

* Login / Register / Profile pages
* Start & Submit Exam flow
* Timer countdown
* Back-to-profile navigation

---

## 📑 API Reference
### 🔐 Auth

#### Register
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "Passw0rd!",
  "full_name": "Student One"
}
```
#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "Passw0rd!"
}
```

#### Profile (Me)
```
GET /api/auth/me
Authorization: Bearer <access_token>
```

#### Refresh Token

```
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

### 📝 Exam
#### Start Exam

```
POST /api/exam/start
Authorization: Bearer <access_token>
```
#### Response:
```
{
  "session_id": 12,
  "questions": [
    {
      "id": 1,
      "text": "What is 2+2?",
      "options": { "A": "3", "B": "4", "C": "5", "D": "6" }
    }
  ]
}
```

#### Submit Exam

```
POST /api/exam/submit
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "session_id": 12,
  "answers": [
    { "question_id": 1, "chosen_option": "B" },
    { "question_id": 2, "chosen_option": "D" }
  ]
}
```

#### Response:

```
{
  "score": 8,
  "total": 10
}
```

---

## 🛢 Database Schema

### **users**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email_enc TEXT NOT NULL,
    email_hash TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    first_login_attempted BOOLEAN DEFAULT FALSE
);
```

### **questions**

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option CHAR(1) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **exam\_sessions**

```sql
CREATE TABLE exam_sessions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    submitted BOOLEAN DEFAULT FALSE,
    score INT DEFAULT 0
);
```

### **exam\_questions**

```sql
CREATE TABLE exam_questions (
    id SERIAL PRIMARY KEY,
    exam_session_id INT REFERENCES exam_sessions(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE
);
```

### **answers**

```sql
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    exam_session_id INT REFERENCES exam_sessions(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    chosen_option CHAR(1)
);
```

### **exams** (alternate historical sessions)

```sql
CREATE TABLE exams (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    duration_minutes INT,
    score INT
);
```

### **exam\_answers** (alternate answer tracking)

```sql
CREATE TABLE exam_answers (
    id SERIAL PRIMARY KEY,
    exam_id INT REFERENCES exams(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    selected_option CHAR(1),
    is_correct BOOLEAN,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **results**

```sql
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    exam_id INT REFERENCES exams(id) ON DELETE CASCADE,
    total_questions INT,
    correct_answers INT,
    score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🖥 UI Pages

* `/` → Login / Register
* `/profile` → User profile + actions
* `/exam` → Take Test (MCQs, timer, submit)

---

## 🧪 Running API Tests

Use the provided Postman collection:

```
backend/postman_collection.json
```

Includes:

* Auth (register, login, refresh)
* Exam (start, submit)

---

## 🔍 Design Choices

* JWT-based authentication with refresh tokens
* PostgreSQL relational schema for users, exams, answers
* Session-based exam flow prevents tampering
* Secure password storage (bcrypt)

---
