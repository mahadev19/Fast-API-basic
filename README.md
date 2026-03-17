# 🏥 Patient Management System API

A simple REST API built using **FastAPI** to manage patient records.
This project demonstrates backend API development with data validation, CRUD operations, and computed fields like BMI.

---

## 🚀 Features

* Create a new patient record
* View all patients
* View a single patient using Patient ID
* Update patient information
* Delete patient records
* Sort patients by height, weight, or BMI
* Automatic BMI calculation
* Automatic health category classification

---

## 🛠 Tech Stack

* Python
* FastAPI
* Pydantic
* JSON (for data storage)
* Uvicorn (ASGI server)

---

## 📂 Project Structure

```
patient-management-api
│
├── main.py            # FastAPI application
├── patients.json      # JSON database for storing patients
├── requirements.txt   # Project dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```
https://github.com/mahadev19/Fast-API-basic.git
```

### 2. Navigate to project folder

```
cd patient-management-api
```

### 3. Create virtual environment

```
python -m venv myenv
```

### 4. Activate virtual environment

Windows:

```
myenv\Scripts\activate
```

Mac/Linux:

```
source myenv/bin/activate
```

### 5. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Running the API

Start the FastAPI server using Uvicorn:

```
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

## 📘 API Documentation

FastAPI automatically provides interactive documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

Alternative documentation:

```
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

### Root Endpoint

```
GET /
```

Returns API welcome message.

---

### View All Patients

```
GET /view
```

Returns all stored patients.

---

### View Single Patient

```
GET /patient/{patient_id}
```

Example:

```
GET /patient/P001
```

---

### Create Patient

```
POST /create
```

Example request body:

```
{
 "id": "P001",
 "name": "John Doe",
 "city": "Mumbai",
 "age": 35,
 "gender": "male",
 "height": 1.75,
 "weight": 70
}
```

---

### Update Patient

```
PUT /edit/{patient_id}
```

Example:

```
PUT /edit/P001
```

---

### Delete Patient

```
DELETE /delete/{patient_id}
```

Example:

```
DELETE /delete/P001
```

---

### Sort Patients

```
GET /sort?sort_by=bmi&order=desc
```

Available sorting fields:

* height
* weight
* bmi

Order options:

* asc
* desc

---

## 🧮 BMI Calculation

BMI is automatically calculated using:

```
BMI = weight / (height²)
```

Based on BMI, the system classifies patients into:

* Underweight
* Normal
* Overweight
* Obese

---

## 🎯 Purpose of the Project

This project was built to practice:

* REST API development
* Data validation using Pydantic
* Backend development using FastAPI
* Basic data persistence using JSON

---

## Authentication and Authorization

This project implements **JWT-based authentication and authorization** to secure API endpoints. It ensures that only authenticated users can access protected routes.

### Authentication

Authentication is the process of verifying **who the user is**.  
In this project, users authenticate themselves by sending their **username and password** to the `/login` endpoint.

If the credentials are correct, the API generates a **JWT (JSON Web Token)** and returns it to the user.

Example login request:

POST /login

Example response:

{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}

The user must use this token to access protected API endpoints.

---

### Authorization

Authorization determines **what resources a user can access** after authentication.

Protected routes require a valid JWT token in the request header.

Example request header:

Authorization: Bearer <your_token>

FastAPI verifies the token before allowing access to the endpoint.

Example of a protected route:

```python
@app.get("/patients")
def get_patients(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route"}
## Database Integration and Migration

In this project, the FastAPI application is integrated with a PostgreSQL database and uses Alembic for database migrations. This setup allows the application to store persistent data and safely manage changes to the database structure over time.

### Database Integration

The application connects to PostgreSQL using SQLAlchemy ORM. SQLAlchemy allows us to interact with the database using Python classes instead of writing raw SQL queries.

**Key components used:**

* FastAPI – API framework
* SQLAlchemy – ORM for database operations
* PostgreSQL – Relational database

The database connection is configured in `database.py`, where the SQLAlchemy engine and session are created.

Example configuration:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

Database models are defined using SQLAlchemy in `models.py`.

Example:

```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
```

This model creates a `users` table in the PostgreSQL database.

---

### Database Migration

Database migrations are managed using Alembic. Migrations help track and apply schema changes such as adding new tables or columns without losing existing data.

Typical migration workflow:

1. Modify the SQLAlchemy model
2. Generate a migration script
3. Apply the migration to the database

Commands used:

```bash
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

Alembic compares the current models with the existing database schema and generates migration scripts automatically.

---

### Project Structure

```
FastAPI/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── alembic.ini
└── requirements.txt
```

---

### API Documentation

After running the server:

```
uvicorn main:app --reload
```

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---
## 🔹 Logging

In this project, logging is implemented to monitor application behavior, track requests, and debug issues effectively. Instead of using print statements, Python’s built-in `logging` module is used.

### Features:

* Logs incoming API requests and response status codes
* Captures errors and exceptions
* Stores logs in a structured format with timestamps
* Helps in debugging and monitoring the application

### Logging Configuration:

* Logging level is set to `INFO`
* Log format includes:

  * Timestamp
  * Log level
  * Message

### Example Log Output:

```
2026-03-17 12:00:01 - INFO - Request: GET /users
2026-03-17 12:00:01 - INFO - Response status: 200
2026-03-17 12:00:05 - ERROR - Error occurred: division by zero
```

### Middleware Logging:

A custom middleware is used to log every request and response:

* Logs HTTP method and endpoint
* Logs response status code

---

## 🔹 API Testing

API testing is implemented to ensure that all endpoints work correctly and handle different scenarios such as success, failure, and authentication.

### Tools Used:

* FastAPI `TestClient`
* Pytest

### Test Coverage:

The following test cases are implemented:

1. **User Creation Test**

   * Verifies that a new user can be created successfully
   * Checks response status and returned data

2. **Error Handling Test**

   * Sends request to an invalid endpoint
   * Ensures API returns `404 Not Found`

3. **Login Test**

   * Verifies user authentication
   * Checks if access token is generated

4. **Protected Route Test**

   * Tests authorization using Bearer token
   * Ensures only authenticated users can access protected endpoints

### Running Tests:

To run all tests, use the following command:

```bash
pytest
```

### Example Output:

```
4 passed in 0.50s
```

### Key Benefits:

* Ensures API reliability
* Detects bugs early
* Validates authentication and authorization
* Helps maintain code quality during updates

---

## 🔹 Project Structure (Testing)

```
project/
│
├── main.py
├── tests/
│   └── test_main.py
```

### Summary

This project demonstrates:

* FastAPI API development
* PostgreSQL database integration
* SQLAlchemy ORM usage
* Alembic database migrations
* CRUD-ready database model setup

## 📜 License

This project is for learning and educational purposes.
