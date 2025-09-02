from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from auth import authenticate_user, create_access_token, bcrypt_context, verify_instructor, verify_client
from sqlalchemy.orm import Session
import models, schemas
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter()

# POST /signup
@router.post("/signup")
def signup(request: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    - Validates if the email is already registered.
    - Hashes the password for secure storage.
    - Saves the user details in the database.
    """
    # Check if the user already exists
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password and create a new user
    hashed_password = bcrypt_context.hash(request.password)
    new_user = models.User(
        username=request.username,
        email=request.email,
        role=request.role,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to log in a user.
    - Authenticates the user using email and password.
    - Generates a JWT token for the authenticated user.
    """
    # Authenticate the user
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate a JWT token
    access_token, expire = create_access_token(user.email, user.id, user.role)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int((expire - datetime.utcnow()).total_seconds())
    }


@router.post('/classes')
def new_classes(request: schemas.ClassCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_instructor)):
    """
    Endpoint to create a new fitness class.
    - Only accessible to instructors.
    - Saves the class details in the database.
    """
    new_class = models.Class(
        name=request.name,
        date_time=request.dateTime,
        instructor=request.instructor,
        available_slots=request.availableSlots
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return {"msg": "Class created successfully", "class_id": new_class.id}


@router.get("/classes")
def upcoming_classes(db: Session = Depends(get_db)):
    """
    Endpoint to fetch all upcoming fitness classes.
    - Returns classes that are scheduled for the future.
    """
    current_time = datetime.utcnow()
    classes = db.query(models.Class).filter(models.Class.date_time > current_time).all()
    return [
        {
            "id": cls.id,
            "name": cls.name,
            "dateTime": cls.date_time,
            "instructor": cls.instructor,
            "availableSlots": cls.available_slots
        }
        for cls in classes
    ]


@router.post("/book")
def book_slot(request: schemas.BookingRequest, db: Session = Depends(get_db), current_user: dict = Depends(verify_client)):
    """
    Endpoint to book a slot in a fitness class.
    - Only accessible to clients.
    - Validates if slots are available and prevents overbooking.
    - Deducts a slot on successful booking.
    """
    # Fetch the class by ID
    fitness_class = db.query(models.Class).filter(models.Class.id == request.class_id).first()

    if not fitness_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    if fitness_class.available_slots <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No slots available for this class"
        )

    # Deduct a slot
    fitness_class.available_slots -= 1

    # Create a booking record
    new_booking = models.Booking(
        class_id=request.class_id,
        client_name=request.client_name,
        client_email=request.client_email
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {
        "msg": "Slot booked successfully",
        "booking_id": new_booking.id,
        "remaining_slots": fitness_class.available_slots
    }


@router.get('/book')
def get_book_classes():
    """
    Placeholder endpoint for fetching booked classes.
    - To be implemented.
    """
    pass


@router.get("/bookings")
def view_user_bookings(db: Session = Depends(get_db), current_user: dict = Depends(verify_client)):
    """
    Endpoint to view all bookings made by the authenticated user.
    - Returns a list of booked classes.
    """
    bookings = db.query(models.Booking).filter(models.Booking.client_email == current_user["username"]).all()
    return [
        {
            "booking_id": booking.id,
            "class_id": booking.class_id,
            "class_name": booking.fitness_class.name,
            "dateTime": booking.fitness_class.date_time,
            "instructor": booking.fitness_class.instructor
        }
        for booking in bookings
    ]