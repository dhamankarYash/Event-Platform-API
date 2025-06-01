from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Tuple, Optional
from datetime import datetime

from models import User, Event, EventRegistration
from schemas import UserCreate, EventCreate, EventUpdate
from auth import get_password_hash

# User CRUD operations
def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email.lower(),  # Store email in lowercase
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email.lower()).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get list of users"""
    return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

# Event CRUD operations
def get_events(db: Session, skip: int = 0, limit: int = 10) -> Tuple[List[Event], int]:
    """Get paginated list of events"""
    total = db.query(Event).count()
    events = (
        db.query(Event)
        .order_by(Event.date_time.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return events, total

def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
    """Get event by ID"""
    return db.query(Event).filter(Event.id == event_id).first()

def create_event(db: Session, event: EventCreate, user_id: int) -> Event:
    """Create a new event"""
    db_event = Event(
        name=event.name,
        description=event.description,
        location=event.location,
        date_time=event.date_time,
        capacity=event.capacity,
        created_by=user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Optional[Event]:
    """Update an event"""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None
    
    update_data = event_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    """Delete an event"""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False

def search_events(
    db: Session, 
    query: str = None, 
    location: str = None,
    skip: int = 0, 
    limit: int = 10
) -> Tuple[List[Event], int]:
    """Search events by name, description, or location"""
    filters = []
    
    if query:
        search_filter = or_(
            Event.name.ilike(f"%{query}%"),
            Event.description.ilike(f"%{query}%")
        )
        filters.append(search_filter)
    
    if location:
        filters.append(Event.location.ilike(f"%{location}%"))
    
    base_query = db.query(Event)
    if filters:
        base_query = base_query.filter(and_(*filters))
    
    total = base_query.count()
    events = (
        base_query
        .order_by(Event.date_time.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return events, total

# Event registration CRUD operations
def register_for_event(db: Session, user_id: int, event_id: int) -> Optional[EventRegistration]:
    """Register a user for an event"""
    # Check if already registered
    existing = db.query(EventRegistration).filter(
        and_(
            EventRegistration.user_id == user_id,
            EventRegistration.event_id == event_id
        )
    ).first()
    
    if existing:
        return None
    
    registration = EventRegistration(
        user_id=user_id,
        event_id=event_id
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def unregister_from_event(db: Session, user_id: int, event_id: int) -> bool:
    """Unregister a user from an event"""
    registration = db.query(EventRegistration).filter(
        and_(
            EventRegistration.user_id == user_id,
            EventRegistration.event_id == event_id
        )
    ).first()
    
    if registration:
        db.delete(registration)
        db.commit()
        return True
    return False

def get_user_registrations(db: Session, user_id: int) -> List[EventRegistration]:
    """Get all registrations for a user"""
    return (
        db.query(EventRegistration)
        .filter(EventRegistration.user_id == user_id)
        .order_by(EventRegistration.registered_at.desc())
        .all()
    )

def get_event_registrations(db: Session, event_id: int) -> List[EventRegistration]:
    """Get all registrations for an event"""
    return (
        db.query(EventRegistration)
        .filter(EventRegistration.event_id == event_id)
        .order_by(EventRegistration.registered_at.asc())
        .all()
    )

def is_user_registered(db: Session, user_id: int, event_id: int) -> bool:
    """Check if user is registered for an event"""
    registration = db.query(EventRegistration).filter(
        and_(
            EventRegistration.user_id == user_id,
            EventRegistration.event_id == event_id
        )
    ).first()
    return registration is not None

def get_event_registration_count(db: Session, event_id: int) -> int:
    """Get the number of registrations for an event"""
    return db.query(EventRegistration).filter(EventRegistration.event_id == event_id).count()
