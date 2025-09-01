from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
import enum
from sqlalchemy.types import Enum as SQLEnum 
from database import Base
from sqlalchemy.orm import relationship


class Role(enum.Enum):
    instructor = 'instructor'
    client = 'client'

# User Table
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    email = Column(String, unique=True, nullable=False)  
    password = Column(String, nullable=False)  
    role = Column(SQLEnum(Role), nullable=False)
    
    # Relationships
    classes = relationship('Classes', back_populates='instructor')
    bookings = relationship('Bookings', back_populates='user')

# Classes Table
class Classes(Base):
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) 
    date_time = Column(DateTime, nullable=False) 
    available_slots = Column(Integer, nullable=False) 
    
    # Foreign Key to User (instructor)
    instructor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    instructor = relationship('User', back_populates='classes')
    bookings = relationship('Bookings', back_populates='fitness_class')

# Bookings Table
class Bookings(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    
    # Client information from booking request
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='bookings')
    fitness_class = relationship('Classes', back_populates='bookings')