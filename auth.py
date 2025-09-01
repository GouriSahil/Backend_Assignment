from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from database import db_dependancy
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])


SECRET_KEY = "f3322270853c880b06d651810a0b8da75acb89fa43d27061591471c5fec9c063"
ALGORITHM = "HS256"

# JWT settings
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Password hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str  # "client" or "instructor"


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int



def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: Optional[timedelta] = None):
    #Create JWT token
    encode = {"sub": username, "id": user_id, "role": role}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=20))
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM), expire


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return {"username": username, "id": user_id, "role": role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

def get_current_active_user(current_user: dict = Depends(get_current_user)):
    # Return current authenticated user
    return current_user


def verify_instructor(current_user: dict = Depends(get_current_user)):
    # Allow only instructors
    if current_user["role"] != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can perform this action"
        )
    return current_user


def verify_client(current_user: dict = Depends(get_current_user)):
    # Allow only clients
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can perform this action"
        )
    return current_user

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependancy, user: CreateUserRequest):
    #Register a new user
    new_user = User(
        username=user.username,
        email=user.email,  
        hashed_password=bcrypt_context.hash(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: db_dependancy = Depends()):
 
    # Login user and generate JWT.
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token, expire = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int((expire - datetime.utcnow()).total_seconds())  
    }

