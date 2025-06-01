from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Import your modules
from database import get_db, engine, Base, test_connection
from models import User, Event, EventRegistration
from schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    EventCreate, EventResponse, EventUpdate,
    EventRegistrationResponse, PaginatedEventsResponse,
    EventWithRegistrationStatus
)
from auth import (
    authenticate_user, create_access_token, get_current_user,
    get_password_hash, verify_password
)
from crud import (
    create_user, get_user_by_email, get_events, get_event_by_id,
    create_event, update_event, delete_event, register_for_event,
    get_user_registrations, unregister_from_event, search_events,
    is_user_registered, get_event_registration_count
)

# Load environment variables
load_dotenv()

# Test database connection before starting
print("🔍 Testing database connection...")
if not test_connection():
    print("❌ Failed to connect to database. Please check your configuration.")
    print("💡 Make sure MySQL is running and credentials in .env are correct")
    exit(1)

# Create database tables
print("📊 Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
except Exception as e:
    print(f"❌ Failed to create database tables: {e}")
    exit(1)

# Create FastAPI app instance
app = FastAPI(
    title=os.getenv("APP_NAME", "Event Discovery Platform API"),
    description="A comprehensive backend system for discovering and registering for local events",
    version=os.getenv("APP_VERSION", "1.0.0"),
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Event Platform Team",
        "email": "support@eventplatform.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add CORS middleware - IMPORTANT: This must come AFTER app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Event Discovery Platform API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running",
        "features": [
            "User Authentication (JWT)",
            "Event Management (CRUD)",
            "Event Registration (RSVP)",
            "Search & Filtering",
            "Pagination",
            "MySQL Database Integration"
        ]
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Authentication endpoints
@app.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account"""
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    try:
        user = create_user(db, user_data)
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )

@app.post("/auth/login", response_model=Token, tags=["Authentication"])
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")

@app.get("/auth/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

# Event endpoints
@app.get("/events", response_model=PaginatedEventsResponse, tags=["Events"])
async def list_events(
    skip: int = Query(0, ge=0, description="Number of events to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of events to return"),
    search: Optional[str] = Query(None, description="Search events by name or description"),
    location: Optional[str] = Query(None, description="Filter events by location"),
    db: Session = Depends(get_db)
):
    """Get paginated list of events with optional search and filtering"""
    try:
        if search or location:
            events, total = search_events(db, query=search, location=location, skip=skip, limit=limit)
        else:
            events, total = get_events(db, skip=skip, limit=limit)
        
        event_responses = []
        for event in events:
            registered_count = get_event_registration_count(db, event.id)
            
            event_response = EventWithRegistrationStatus(
                id=event.id,
                name=event.name,
                description=event.description,
                location=event.location,
                date_time=event.date_time,
                capacity=event.capacity,
                registered_count=registered_count,
                created_by=event.created_by,
                created_at=event.created_at,
                is_registered=False  # Default for non-authenticated users
            )
            event_responses.append(event_response)
        
        return PaginatedEventsResponse(
            events=event_responses,
            total=total,
            skip=skip,
            limit=limit,
            has_next=skip + limit < total,
            has_prev=skip > 0
        )
    except Exception as e:
        print(f"Error in list_events: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch events"
        )

@app.get("/events/{event_id}", response_model=EventWithRegistrationStatus, tags=["Events"])
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific event"""
    event = get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    registered_count = get_event_registration_count(db, event.id)
    
    return EventWithRegistrationStatus(
        id=event.id,
        name=event.name,
        description=event.description,
        location=event.location,
        date_time=event.date_time,
        capacity=event.capacity,
        registered_count=registered_count,
        created_by=event.created_by,
        created_at=event.created_at,
        is_registered=False
    )

@app.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED, tags=["Events"])
async def create_new_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new event (authenticated users only)"""
    try:
        event = create_event(db, event_data, current_user.id)
        return EventResponse(
            id=event.id,
            name=event.name,
            description=event.description,
            location=event.location,
            date_time=event.date_time,
            capacity=event.capacity,
            registered_count=0,
            created_by=event.created_by,
            created_at=event.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event"
        )

# Event registration endpoints
@app.post("/events/{event_id}/register", response_model=EventRegistrationResponse, tags=["Event Registration"])
async def register_for_event_endpoint(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register for an event"""
    event = get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if event is full
    current_registrations = get_event_registration_count(db, event_id)
    if current_registrations >= event.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is full"
        )
    
    # Check if user is already registered
    if is_user_registered(db, current_user.id, event_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this event"
        )
    
    registration = register_for_event(db, current_user.id, event_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register for event"
        )
    
    return EventRegistrationResponse(
        id=registration.id,
        user_id=registration.user_id,
        event_id=registration.event_id,
        registered_at=registration.registered_at
    )

@app.delete("/events/{event_id}/register", status_code=status.HTTP_204_NO_CONTENT, tags=["Event Registration"])
async def unregister_from_event_endpoint(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unregister from an event"""
    success = unregister_from_event(db, current_user.id, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )

@app.get("/my-registrations", response_model=List[EventRegistrationResponse], tags=["Event Registration"])
async def get_my_registrations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's event registrations"""
    registrations = get_user_registrations(db, current_user.id)
    return [
        EventRegistrationResponse(
            id=reg.id,
            user_id=reg.user_id,
            event_id=reg.event_id,
            registered_at=reg.registered_at
        )
        for reg in registrations
    ]

@app.get("/my-events", response_model=List[EventResponse], tags=["Events"])
async def get_my_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get events created by current user"""
    events = db.query(Event).filter(Event.created_by == current_user.id).all()
    
    event_responses = []
    for event in events:
        registered_count = get_event_registration_count(db, event.id)
        event_responses.append(EventResponse(
            id=event.id,
            name=event.name,
            description=event.description,
            location=event.location,
            date_time=event.date_time,
            capacity=event.capacity,
            registered_count=registered_count,
            created_by=event.created_by,
            created_at=event.created_at
        ))
    
    return event_responses

# Admin endpoint for debugging (remove in production)
@app.get("/admin/stats", tags=["Admin"])
async def get_admin_stats(db: Session = Depends(get_db)):
    """Get database statistics for debugging"""
    try:
        total_users = db.query(User).count()
        total_events = db.query(Event).count()
        total_registrations = db.query(EventRegistration).count()
        
        # Get recent users
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
        
        # Get recent events
        recent_events = db.query(Event).order_by(Event.created_at.desc()).limit(5).all()
        
        return {
            "stats": {
                "total_users": total_users,
                "total_events": total_events,
                "total_registrations": total_registrations
            },
            "recent_users": [
                {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "created_at": user.created_at
                }
                for user in recent_users
            ],
            "recent_events": [
                {
                    "id": event.id,
                    "name": event.name,
                    "location": event.location,
                    "date_time": event.date_time,
                    "capacity": event.capacity,
                    "created_by": event.created_by,
                    "created_at": event.created_at
                }
                for event in recent_events
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )

# Admin endpoints for data management
@app.get("/admin/users", tags=["Admin"])
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users (admin only)"""
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in users
    ]

@app.delete("/admin/users/{user_id}", tags=["Admin"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}

@app.put("/admin/users/{user_id}", tags=["Admin"])
async def update_user(user_id: int, full_name: str = None, email: str = None, db: Session = Depends(get_db)):
    """Update a user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    
    db.commit()
    db.refresh(user)
    return {"message": f"User {user_id} updated successfully", "user": {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }}

@app.get("/admin/events", tags=["Admin"])
async def get_all_events_admin(db: Session = Depends(get_db)):
    """Get all events with creator info (admin only)"""
    events = db.query(Event).join(User).all()
    return [
        {
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "location": event.location,
            "date_time": event.date_time,
            "capacity": event.capacity,
            "created_by": event.created_by,
            "creator_name": event.creator.full_name,
            "creator_email": event.creator.email,
            "created_at": event.created_at,
            "registered_count": get_event_registration_count(db, event.id)
        }
        for event in events
    ]

@app.delete("/admin/events/{event_id}", tags=["Admin"])
async def delete_event_admin(event_id: int, db: Session = Depends(get_db)):
    """Delete an event (admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return {"message": f"Event {event_id} deleted successfully"}

@app.put("/admin/events/{event_id}", tags=["Admin"])
async def update_event_admin(
    event_id: int, 
    name: str = None,
    description: str = None,
    location: str = None,
    capacity: int = None,
    db: Session = Depends(get_db)
):
    """Update an event (admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if name:
        event.name = name
    if description:
        event.description = description
    if location:
        event.location = location
    if capacity:
        event.capacity = capacity
    
    db.commit()
    db.refresh(event)
    return {"message": f"Event {event_id} updated successfully", "event": {
        "id": event.id,
        "name": event.name,
        "description": event.description,
        "location": event.location,
        "capacity": event.capacity
    }}

@app.get("/admin/registrations", tags=["Admin"])
async def get_all_registrations(db: Session = Depends(get_db)):
    """Get all registrations (admin only)"""
    registrations = db.query(EventRegistration).join(User).join(Event).all()
    return [
        {
            "id": reg.id,
            "user_id": reg.user_id,
            "user_name": reg.user.full_name,
            "user_email": reg.user.email,
            "event_id": reg.event_id,
            "event_name": reg.event.name,
            "registered_at": reg.registered_at
        }
        for reg in registrations
    ]

@app.delete("/admin/registrations/{registration_id}", tags=["Admin"])
async def delete_registration_admin(registration_id: int, db: Session = Depends(get_db)):
    """Delete a registration (admin only)"""
    registration = db.query(EventRegistration).filter(EventRegistration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    db.delete(registration)
    db.commit()
    return {"message": f"Registration {registration_id} deleted successfully"}

# Run the application
if __name__ == "__main__":
    print("🚀 Starting Event Discovery Platform API...")
    print(f"📊 API Documentation: http://127.0.0.1:8080/docs")
    print(f"📖 Alternative Docs: http://127.0.0.1:8080/redoc")
    print(f"🌐 Frontend should connect to: http://127.0.0.1:8080")
    
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8080, 
        reload=True,
        log_level="info"
    )
