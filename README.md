# Event Platform API
# Event Discovery Platform API - MySQL Edition

A complete FastAPI backend system for discovering and registering for local events, configured for MySQL database.

## 🚀 Features

- **User Authentication**: JWT-based signup/login with secure password hashing
- **Event Management**: Full CRUD operations for events with search and filtering
- **Event Registration**: Users can register/unregister for events (RSVP system)
- **MySQL Integration**: Optimized for MySQL with proper indexing and relationships
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Data Validation**: Comprehensive input validation using Pydantic
- **Pagination**: Efficient pagination for large datasets
- **Search & Filter**: Search events by name, description, and location

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy with MySQL optimizations
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic models with custom validators
- **Documentation**: FastAPI auto-generated docs

## 📁 Project Structure

\`\`\`
event-platform-api/
├── main.py              # FastAPI application and route definitions
├── models.py            # SQLAlchemy database models with MySQL optimizations
├── schemas.py           # Pydantic schemas for request/response validation
├── database.py          # MySQL database configuration and connection
├── auth.py              # JWT authentication utilities
├── crud.py              # Database CRUD operations
├── test_connection.py   # Database connection test script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore file
└── README.md           # This file
\`\`\`

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+
- pip (Python package manager)

### 2. MySQL Setup

\`\`\`sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE event_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create application user
CREATE USER 'event_user'@'localhost' IDENTIFIED BY 'event_password123';
GRANT ALL PRIVILEGES ON event_platform.* TO 'event_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify setup
SHOW DATABASES;
EXIT;
\`\`\`

### 3. Project Setup

\`\`\`bash
# Clone or create project directory
mkdir event-platform-api
cd event-platform-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 4. Configuration

The `.env` file is already configured with default values. Update if needed:

\`\`\`env
DATABASE_URL=mysql+pymysql://event_user:event_password123@localhost:3306/event_platform
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-make-it-long-and-random
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

### 5. Test Database Connection

\`\`\`bash
python test_connection.py
\`\`\`

You should see:
\`\`\`
🔍 Testing Event Discovery Platform Database Connection
==================================================
1. Testing basic database connection...
✅ Database connection successful!
2. Testing table creation...
✅ Tables created successfully!
3. Checking if tables exist...
✅ Table 'users' exists
✅ Table 'events' exists
✅ Table 'event_registrations' exists
4. Testing basic database operations...
✅ Database operations working!

🎉 All database tests passed!
\`\`\`

### 6. Run the Application

\`\`\`bash
python main.py
\`\`\`

The API will be available at:
- **API**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and get access token |
| GET | `/auth/me` | Get current user information |

### Event Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events` | Get paginated list of events with search/filter |
| GET | `/events/{event_id}` | Get specific event details |
| POST | `/events` | Create a new event (authenticated) |
| PUT | `/events/{event_id}` | Update an event (creator only) |
| DELETE | `/events/{event_id}` | Delete an event (creator only) |
| GET | `/my-events` | Get events created by current user |

### Event Registration Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/events/{event_id}/register` | Register for an event |
| DELETE | `/events/{event_id}/register` | Unregister from an event |
| GET | `/my-registrations` | Get user's event registrations |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check with database status |

## 🧪 Testing the API

### 1. Create a User

\`\`\`bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "full_name": "John Doe",
       "password": "securepassword123"
     }'
\`\`\`

### 2. Login

\`\`\`bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "password": "securepassword123"
     }'
\`\`\`

Save the `access_token` from the response.

### 3. Create an Event

\`\`\`bash
curl -X POST "http://localhost:8000/events" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
       "name": "Tech Meetup 2024",
       "description": "A gathering of tech enthusiasts to discuss latest trends",
       "location": "San Francisco, CA",
       "date_time": "2024-06-15T18:00:00",
       "capacity": 50
     }'
\`\`\`

### 4. Get Events with Search

\`\`\`bash
# Get all events
curl "http://localhost:8000/events?skip=0&limit=10"

# Search events
curl "http://localhost:8000/events?search=tech&location=san francisco"
\`\`\`

### 5. Register for an Event

\`\`\`bash
curl -X POST "http://localhost:8000/events/1/register" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
\`\`\`

## 🗄️ Database Schema

### Users Table
\`\`\`sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (email),
    INDEX idx_user_active (is_active)
);
\`\`\`

### Events Table
\`\`\`sql
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL,
    capacity INT NOT NULL,
    created_by INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_event_date (date_time),
    INDEX idx_event_location (location),
    INDEX idx_event_creator (created_by)
);
\`\`\`

### Event Registrations Table
\`\`\`sql
CREATE TABLE event_registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    UNIQUE KEY idx_registration_unique (user_id, event_id),
    INDEX idx_registration_user (user_id),
    INDEX idx_registration_event (event_id)
);
\`\`\`

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://event_user:event_password123@localhost:3306/event_platform` |
| `SECRET_KEY` | JWT secret key | Required - set a strong key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `APP_NAME` | Application name | `Event Discovery Platform API` |
| `APP_VERSION` | Application version | `1.0.0` |
| `DEBUG` | Debug mode | `True` |

### MySQL Configuration

For production, consider these MySQL settings in your `my.cnf`:

\`\`\`ini
[mysqld]
# Connection settings
max_connections = 200
connect_timeout = 10
wait_timeout = 600
max_allowed_packet = 64M

# Performance settings
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2

# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
\`\`\`

## 🚀 Production Deployment

### 1. Security Checklist

- [ ] Change `SECRET_KEY` to a strong, random value
- [ ] Use environment variables for all sensitive data
- [ ] Enable HTTPS
- [ ] Restrict CORS origins
- [ ] Use a production MySQL server
- [ ] Set up proper logging
- [ ] Configure firewall rules

### 2. Production Server Setup

\`\`\`bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
\`\`\`

### 3. Docker Deployment (Optional)

\`\`\`dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
\`\`\`

## 🐛 Troubleshooting

### Common Issues

1. **Connection Refused**
   \`\`\`
   pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
   \`\`\`
   - Ensure MySQL is running: `sudo systemctl start mysql`
   - Check MySQL port (default 3306)

2. **Access Denied**
   \`\`\`
   pymysql.err.OperationalError: (1045, "Access denied for user")
   \`\`\`
   - Verify username/password in `.env`
   - Check user permissions in MySQL

3. **Database Not Found**
   \`\`\`
   pymysql.err.OperationalError: (1049, "Unknown database")
   \`\`\`
   - Create the database: `CREATE DATABASE event_platform;`

4. **Table Creation Errors**
   - Run `python test_connection.py` to diagnose
   - Check MySQL user permissions

### Debug Mode

Enable debug logging by setting in `.env`:
\`\`\`env
DEBUG=True
\`\`\`

Then check logs for detailed error information.

## 📈 Performance Tips

1. **Database Indexing**: The models include optimized indexes for common queries
2. **Connection Pooling**: Configured in `database.py`
3. **Pagination**: Always use pagination for large datasets
4. **Query Optimization**: Use the search endpoints efficiently

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check this README
2. Run `python test_connection.py` for database issues
3. Check the `/health` endpoint for system status
4. Review logs for error details

---






