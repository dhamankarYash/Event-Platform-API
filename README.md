# 🎉 Event Platform - Full Stack Application
### 🌍 *Discover & Register for Events — FastAPI Backend + React Frontend*

A complete **full-stack event discovery and registration platform** with secure authentication, advanced filtering, and modern UI/UX.

---

## 🚀 Features

✅ **JWT Authentication (Email + Password Login)**  
✅ **Event CRUD + Filtering**  
✅ **User Registrations (RSVP)**  
✅ **MySQL + SQLAlchemy Backend**  
✅ **React + TypeScript Frontend**  
✅ **Responsive Design with Tailwind CSS**  
✅ **OpenAPI Documentation**  
✅ **Pagination + Search**  
✅ **Real-time Event Updates**  
✅ **User Dashboard & Profile Management**

---

## 🛠 Tech Stack

### Backend
| Tool         | Purpose                           |
|--------------|------------------------------------|
| 🔥 FastAPI    | Web framework (high performance)   |
| 🐬 MySQL      | Relational database                |
| 🛠 SQLAlchemy | ORM for DB models                  |
| 🔐 JWT        | Auth tokens                        |
| 🔑 bcrypt     | Password hashing                   |
| 📘 Pydantic   | Data validation                    |

### Frontend
| Tool         | Purpose                           |
|--------------|------------------------------------|
| ⚛️ React      | UI library                         |
| 📘 TypeScript | Type safety                        |
| 🎨 Tailwind   | CSS framework                      |
| 🔄 Axios      | HTTP client                        |
| 🧭 React Router | Client-side routing              |
| 🎯 Context API | State management                  |

---

## 📁 Project Structure

```bash
event-platform/
├── backend/                    # FastAPI Backend
│   ├── main.py                # FastAPI routes
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── database.py            # MySQL DB config
│   ├── auth.py                # JWT authentication
│   ├── crud.py                # CRUD operations
│   ├── test_connection.py     # DB health check
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── README.md
│
└── frontend/                   # React Frontend
    ├── public/
    │   ├── index.html         # HTML template with Tailwind CDN
    │   └── favicon.ico
    ├── src/
    │   ├── components/        # Reusable UI components
    │   │   ├── common/
    │   │   │   ├── Header.tsx
    │   │   │   ├── Footer.tsx
    │   │   │   ├── Loading.tsx
    │   │   │   └── Modal.tsx
    │   │   ├── auth/
    │   │   │   ├── LoginForm.tsx
    │   │   │   ├── SignupForm.tsx
    │   │   │   └── ProtectedRoute.tsx
    │   │   └── events/
    │   │       ├── EventCard.tsx
    │   │       ├── EventList.tsx
    │   │       ├── EventForm.tsx
    │   │       └── EventDetails.tsx
    │   ├── pages/
    │   │   ├── Home.tsx
    │   │   ├── Events.tsx
    │   │   ├── EventDetail.tsx
    │   │   ├── Login.tsx
    │   │   ├── Signup.tsx
    │   │   ├── Dashboard.tsx
    │   │   ├── Profile.tsx
    │   │   └── CreateEvent.tsx
    │   ├── services/
    │   │   ├── api.ts
    │   │   ├── authService.ts
    │   │   ├── eventService.ts
    │   │   └── userService.ts
    │   ├── contexts/
    │   │   ├── AuthContext.tsx
    │   │   └── EventContext.tsx
    │   ├── types/
    │   │   ├── auth.ts
    │   │   ├── event.ts
    │   │   └── user.ts
    │   ├── utils/
    │   │   ├── constants.ts
    │   │   ├── helpers.ts
    │   │   └── validation.ts
    │   ├── hooks/
    │   │   ├── useAuth.ts
    │   │   └── useEvents.ts
    │   ├── App.tsx
    │   ├── index.tsx
    │   └── index.css
    ├── package.json
    ├── tsconfig.json
    └── tailwind.config.js
```


---

## ✅ Prerequisites

- **Backend**: Python 3.8+, MySQL 5.7+
- **Frontend**: Node.js 16+, npm/yarn
- Git

---

## 🚀 Quick Start

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourname/event-platform.git
cd event-platform
```

### 2️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials

# Test database connection
python test_connection.py

# Start backend server
uvicorn main:app --reload
```

**Backend runs on**: http://localhost:8000

### 3️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Frontend runs on**: http://localhost:3000

---

## 💾 Database Setup

```sql
CREATE DATABASE event_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'event_user'@'localhost' IDENTIFIED BY 'event_password123';
GRANT ALL PRIVILEGES ON event_platform.* TO 'event_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## 🔐 Environment Configuration

### Backend `.env`

```env
DATABASE_URL=mysql+pymysql://event_user:event_password123@localhost:3306/event_platform
SECRET_KEY=your-super-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000
```

### Frontend `.env`

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=Event Platform
```

---

## 📚 API Endpoints

### 🔑 Authentication

| Method | Endpoint     | Description           |
|--------|--------------|-----------------------|
| POST   | /auth/signup | Register new user     |
| POST   | /auth/login  | Login & get JWT       |
| GET    | /auth/me     | Get current user      |

### 📅 Events

| Method | Endpoint        | Description                       |
|--------|-----------------|-----------------------------------|
| GET    | /events         | List events (search & filter)     |
| GET    | /events/{id}    | Get event details                 |
| POST   | /events         | Create event (auth required)      |
| PUT    | /events/{id}    | Update event                      |
| DELETE | /events/{id}    | Delete event                      |
| GET    | /my-events      | User's created events             |

### 📝 Registrations

| Method | Endpoint                  | Description        |
|--------|---------------------------|--------------------|
| POST   | /events/{id}/register     | Register for event |
| DELETE | /events/{id}/register     | Cancel registration|
| GET    | /my-registrations         | User's registrations|

---

## 🎨 Frontend Components

### 🔧 Core Components

#### AuthContext.tsx

```typescript
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signup: (userData: SignupData) => Promise<void>;
  loading: boolean;
}
```

#### EventCard.tsx

```typescript
interface EventCardProps {
  event: Event;
  onRegister?: (eventId: number) => void;
  showActions?: boolean;
}
```

#### ProtectedRoute.tsx

```typescript
interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}
```

### 📱 Pages Structure

- **Home**: Landing page with featured events
- **Events**: Searchable event listings with filters
- **EventDetail**: Detailed event view with registration
- **Dashboard**: User's events and registrations
- **Profile**: User profile management
- **Login/Signup**: Authentication forms

---

## 🔄 Development Workflow

### 1️⃣ Start Development Servers

```bash
# Terminal 1 - Backend
cd backend && uvicorn main:app --reload

# Terminal 2 - Frontend  
cd frontend && npm start
```

### 2️⃣ API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3️⃣ Testing

```bash
# Backend tests
cd backend && python -m pytest

# Frontend tests
cd frontend && npm test
```

---

## 🚀 Deployment

### Backend (FastAPI)

```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend (React)

```bash
# Build for production
npm run build

# Serve static files
npm install -g serve
serve -s build
```

---

## 🔒 Security Features

- ✅ JWT token authentication
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ✅ Input validation & sanitization
- ✅ Protected routes
- ✅ SQL injection prevention

---

## 🎯 Key Features Implementation

### Authentication Flow

1. User signs up/logs in via frontend
2. Backend validates credentials & returns JWT
3. Frontend stores token & includes in API requests
4. Protected routes check authentication status

### Event Management

1. Users can create, edit, delete their events
2. Public event browsing with search/filter
3. Event registration with capacity limits
4. Real-time registration updates

### User Experience

1. Responsive design for all devices
2. Loading states and error handling
3. Form validation and feedback
4. Intuitive navigation and UI

---

## 🛠 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| CORS errors | Check CORS_ORIGINS in backend .env |
| Database connection | Verify MySQL is running & credentials |
| Frontend API calls fail | Ensure REACT_APP_API_URL is correct |
| Authentication issues | Check JWT token expiration |

### Development Tips

- Use browser dev tools for debugging API calls
- Check backend logs for detailed error messages
- Ensure both servers are running on correct ports
- Clear browser cache if experiencing issues

---


# 📦 Backend Requirements — Event Platform

This document lists and explains the backend dependencies used in the **FastAPI-based** Event Platform.

---

## 🧰 Core Dependencies

| Package             | Version   | Purpose                              |
|---------------------|-----------|--------------------------------------|
| `fastapi`           | 0.104.1   | Web framework for building APIs      |
| `uvicorn[standard]` | 0.24.0    | ASGI server to run FastAPI apps      |
| `sqlalchemy`        | 2.0.23    | ORM for working with MySQL DB        |
| `python-multipart`  | 0.0.6     | Handle file uploads                  |
| `python-dotenv`     | 1.0.0     | Load environment variables from `.env` |

---

## 🔐 Authentication & Security

| Package                         | Version   | Purpose                        |
|----------------------------------|-----------|--------------------------------|
| `python-jose[cryptography]`     | 3.3.0     | JWT encoding and decoding      |
| `passlib[bcrypt]`               | 1.7.4     | Password hashing with bcrypt   |
| `email-validator`               | 2.1.0     | Validate email addresses       |

---

## 📊 Data Validation

| Package            | Version   | Purpose                        |
|--------------------|-----------|--------------------------------|
| `pydantic[email]`  | 2.5.0     | Schema validation and typing   |

---

## 🐬 MySQL Driver

| Package   | Version   | Purpose                          |
|-----------|-----------|----------------------------------|
| `pymysql` | 1.1.0     | MySQL client used by SQLAlchemy  |

---


## 👥 Team

- **Backend**: FastAPI + MySQL
- **Frontend**: React + TypeScript + Tailwind
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT tokens

