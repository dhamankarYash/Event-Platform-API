# 🎉 Event Platform API  
### 🌍 *Discover & Register for Events — FastAPI + MySQL Edition*

A complete **FastAPI backend system** to power an event discovery and registration platform with secure authentication, advanced filtering, and MySQL integration.

---

## 🚀 Features

✅ **JWT Authentication**  
✅ **Event CRUD + Filtering**  
✅ **User Registrations (RSVP)**  
✅ **MySQL + SQLAlchemy**  
✅ **OpenAPI Docs**  
✅ **Pagination + Search**  
✅ **Fully Validated APIs**

---

## 🛠 Tech Stack

| Tool        | Purpose                        |
|-------------|--------------------------------|
| 🔥 FastAPI   | Web framework (high performance) |
| 🐬 MySQL     | Relational database             |
| 🛠 SQLAlchemy| ORM for DB models               |
| 🔐 JWT       | Auth tokens                     |
| 🔑 bcrypt    | Password hashing                |
| 📘 Pydantic  | Data validation                 |

---

## 📁 Project Structure

```
event-platform-api/
├── main.py              # FastAPI routes
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── database.py          # MySQL DB config
├── auth.py              # JWT authentication
├── crud.py              # CRUD operations
├── test_connection.py   # DB health check
├── requirements.txt     # Python dependencies
├── .env                 # Env vars
├── .gitignore
└── README.md
```

# ⚡ Quick Start

## ✅ Prerequisites
- Python 3.8+
- MySQL 5.7 or higher
- `pip` installed

---

## 💾 MySQL Setup

```sql
CREATE DATABASE event_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'event_user'@'localhost' IDENTIFIED BY 'event_password123';
GRANT ALL PRIVILEGES ON event_platform.* TO 'event_user'@'localhost';
FLUSH PRIVILEGES;
```

---


## 💾 MySQL Setup

```sql
CREATE DATABASE event_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'event_user'@'localhost' IDENTIFIED BY 'event_password123';
GRANT ALL PRIVILEGES ON event_platform.* TO 'event_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## ⚙️ Project Setup

```bash
# Clone and navigate
git clone https://github.com/yourname/event-platform-api.git
cd event-platform-api

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Configure `.env`

```
DATABASE_URL=mysql+pymysql://event_user:event_password123@localhost:3306/event_platform
SECRET_KEY=change-this-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🧪 Test DB Connection

```bash
python test_connection.py
```

---

## ▶️ Run the API

```bash
python main.py
```

📍 Access the API:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📚 API Reference

### 🔑 Auth

| Method | Endpoint     | Description           |
|--------|--------------|-----------------------|
| POST   | /auth/signup | Register a new user   |
| POST   | /auth/login  | Login & get JWT       |
| GET    | /auth/me     | Get current user info |

### 📅 Events

| Method | Endpoint        | Description                       |
|--------|------------------|-----------------------------------|
| GET    | /events          | List events with search & filter |
| GET    | /events/{id}     | View event details               |
| POST   | /events          | Create an event (auth required)  |
| PUT    | /events/{id}     | Update your event                |
| DELETE | /events/{id}     | Delete your event                |
| GET    | /my-events       | Your created events              |

### 📝 Registration

| Method | Endpoint                  | Description         |
|--------|---------------------------|---------------------|
| POST   | /events/{id}/register     | RSVP for an event   |
| DELETE | /events/{id}/register     | Cancel RSVP         |
| GET    | /my-registrations         | See your registrations |

### 🔧 Utilities

| Method | Endpoint  | Description             |
|--------|-----------|-------------------------|
| GET    | /         | App info                |
| GET    | /health   | DB & API health check   |

---

## 🧪 Testing the API

### 1️⃣ Signup

```bash
curl -X POST http://localhost:8000/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"john@example.com", "full_name":"John Doe", "password":"123456"}'
```

### 2️⃣ Login

```bash
curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"john@example.com", "password":"123456"}'
```

### 3️⃣ Create an Event

```bash
curl -X POST http://localhost:8000/events \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name":"Tech Meetup", "description":"...", "location":"NYC", "date_time":"2024-06-15T18:00:00", "capacity":100}'
```

---

## 🗄️ Database Schema (MySQL)

### 👤 `users`

```sql
id INT PRIMARY KEY AUTO_INCREMENT,
email VARCHAR(255) UNIQUE NOT NULL,
full_name VARCHAR(255),
hashed_password VARCHAR(255),
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### 🎫 `events`

```sql
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255),
description TEXT,
location VARCHAR(255),
date_time DATETIME,
capacity INT,
created_by INT,
FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
```

### ✅ `event_registrations`

```sql
id INT PRIMARY KEY AUTO_INCREMENT,
user_id INT,
event_id INT,
registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
UNIQUE(user_id, event_id),
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (event_id) REFERENCES events(id)
```

---

## 🔒 Security Checklist (Production)

- ✅ Use a strong `SECRET_KEY`
- ✅ Use env variables for secrets
- ✅ Enable HTTPS
- ✅ Restrict CORS origins
- ✅ Use production-grade MySQL
- ✅ Add logging and monitoring

---

## 🚀 Deployment

### 🔧 Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

---

## 🛠 Troubleshooting

| Error                      | Solution                                  |
|---------------------------|-------------------------------------------|
| Can't connect to MySQL    | Ensure MySQL is running & port 3306 is open |
| Access denied             | Check DB user & password in `.env`         |
| Unknown database          | Run `CREATE DATABASE event_platform;`      |
| Table creation fails      | Run `python test_connection.py` to debug   |
