# Starlabs Assignment

## Project Overview
Welcome to the Starlabs Assignment! This project is a Python-based web application designed to manage fitness classes and bookings. It provides user authentication, class scheduling, and booking functionalities through a set of well-defined API endpoints. The application is built with simplicity and scalability in mind, making it easy to extend and maintain.

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- `uv` (Python dependency management tool)
- SQLite (or any other database of your choice)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/GouriSahil/Backend_Assignment.git
   cd Backend_Assignment
   ```
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
   The `uv` tool will automatically install all dependencies listed in the `pyproject.toml` file. No need to manually activate a virtual environment—`uv` handles it for you.

### Database Initialization
1. Initialize the database:
   ```bash
   uv run init_db.py
   ```
   This will initialize the database and create the required tables.
2. Verify that the database file (e.g., `fitness_booking.db`) has been created in the project directory.

   If you are using a different database (e.g., PostgreSQL, MySQL), update the database connection settings in `database.py` accordingly.

## How to Run Locally
1. Start the application:
   ```bash
   uv run main.py
   ```
2. The server will start on `http://127.0.0.1:8000` by default.
3. Access the application by navigating to the base URL in your browser or using API tools like Postman.

## API Usage

### Base URL
`http://127.0.0.1:8000`

### Endpoints

#### 1. Signup
**Endpoint:** `/signup`

**Method:** `POST`

**Request Body:**
```json
{
  "username": "example_user",
  "email": "example_email@example.com",
  "password": "example_password",
  "role": "client"
}
```

**Response:**
```json
{
  "msg": "User created successfully"
}
```

#### 2. Login
**Endpoint:** `/login`

**Method:** `POST`

**Request Body:**
```json
{
  "username": "example_email@example.com",
  "password": "example_password"
}
```

**Response:**
```json
{
  "access_token": "your_auth_token",
  "token_type": "bearer",
  "expires_in": 1200
}
```

#### 3. Create New Fitness Class
**Endpoint:** `/classes`

**Method:** `POST`

**Headers:**
```json
{
  "Authorization": "Bearer your_auth_token"
}
```

**Request Body:**
```json
{
  "name": "Yoga",
  "dateTime": "2025-09-02T10:00:00",
  "instructor": "John Doe",
  "availableSlots": 20
}
```

**Response:**
```json
{
  "msg": "Class created successfully",
  "class_id": 1
}
```

#### 4. Fetch Upcoming Classes
**Endpoint:** `/classes`

**Method:** `GET`

**Response:**
```json
[
  {
    "id": 1,
    "name": "Yoga",
    "dateTime": "2025-09-02T10:00:00",
    "instructor": "John Doe",
    "availableSlots": 20
  }
]
```

#### 5. Book a Slot
**Endpoint:** `/book`

**Method:** `POST`

**Headers:**
```json
{
  "Authorization": "Bearer your_auth_token"
}
```

**Request Body:**
```json
{
  "class_id": 1,
  "client_name": "Alice",
  "client_email": "alice@example.com"
}
```

**Response:**
```json
{
  "msg": "Slot booked successfully",
  "booking_id": 1,
  "remaining_slots": 19
}
```

#### 6. View All Bookings by Authenticated User
**Endpoint:** `/bookings`

**Method:** `GET`

**Headers:**
```json
{
  "Authorization": "Bearer your_auth_token"
}
```

**Response:**
```json
[
  {
    "booking_id": 1,
    "class_id": 1,
    "class_name": "Yoga",
    "dateTime": "2025-09-02T10:00:00",
    "instructor": "John Doe"
  }
]
```

### Postman Sample
1. Open Postman and create a new request.
2. For each endpoint:
   - Set the method (e.g., `POST`, `GET`).
   - Use the corresponding URL (e.g., `http://127.0.0.1:8000/signup`).
   - Add headers if required (e.g., `Authorization: Bearer your_auth_token`).
   - Add the request body in `raw` format and set the type to `JSON`.
3. Send the request and verify the response.

You can now use these endpoints to interact with the application.