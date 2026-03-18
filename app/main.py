# Import required libraries
from fastapi import FastAPI, Path, HTTPException, Query, Depends, Request, Header, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import os
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import verify_password, create_access_token, oauth2_scheme, fake_users_db
from app.logger import logger
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from app import models
from app import crud
from app import schemas
from app.database import engine, SessionLocal, Base
from app.core.settings import settings
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

# -------------------------------
# APP INITIALIZATION
# -------------------------------
app = FastAPI()

# -------------------------------
# PROMETHEUS METRICS
# -------------------------------
Instrumentator().instrument(app).expose(app)

REQUEST_COUNT = Counter("my_requests_total", "Total Requests")

# -------------------------------
# CREATE DB TABLES
# -------------------------------

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning(f"Could not create DB tables: {e}")
# -------------------------------
# RATE LIMITER SETUP
# -------------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )

# -------------------------------
# MIDDLEWARE (LOGGING)
# -------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# -------------------------------
# DATABASE DEPENDENCY
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# BACKGROUND TASK HELPER
# -------------------------------
def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

# -------------------------------
# ROOT
# -------------------------------
@app.get("/")
@limiter.limit("5/minute")
def hello(request: Request):
    logger.info("Root endpoint accessed")
    return {'message': 'Patient Management System API'}

# -------------------------------
# ABOUT
# -------------------------------
@app.get("/about")
def about():
    return {'message': 'A Fully Functional API to manage your patient records'}

# -------------------------------
# ERROR TEST
# -------------------------------
@app.get("/error")
def error_example():
    try:
        x = 10 / 0
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {"error": "Something went wrong"}

# -------------------------------
# BACKGROUND TASK TEST
# -------------------------------
@app.get("/test")
async def test(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "User accessed /test")
    return {"message": "Response sent immediately"}

# -------------------------------
# CUSTOM PROMETHEUS METRIC
# -------------------------------
@app.get("/custom")
def custom():
    REQUEST_COUNT.inc()
    return {"message": "Tracked endpoint"}

# -------------------------------
# LOGIN (RATE LIMITED)
# -------------------------------
@app.post("/login")
@limiter.limit("3/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):

    user = fake_users_db.get(form_data.username)

    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# -------------------------------
# PROTECTED ROUTE
# -------------------------------
@app.get("/protected")
def protected(authorization: str = Header(None)):

    expected = f"Bearer {settings.SECRET_TOKEN}"     # ← FIXED (was SECRET_KEY)

    if authorization != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"message": "Protected route"}

# -------------------------------
# PATIENTS (protected with oauth2)
# -------------------------------
@app.get("/patients")
async def get_patients(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected route"}

# -------------------------------
# USER CREATION (DB)
# -------------------------------
@app.post("/users")
@limiter.limit("5/minute")
async def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


# -------------------------------
# PATIENT MODEL
# -------------------------------
class Patient(BaseModel):

    id: Annotated[str, Field(..., description='Id of the patient', example='P001')]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[
        Literal['male', 'female', 'others'],
        Field(..., description="Gender of the patient")
    ]
    height: Annotated[float, Field(..., gt=0, description='Height of the Patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the Patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return "Overweight"
        else:
            return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# -------------------------------
# FILE HANDLING
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "patients.json")

def load_data():
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------------
# PATIENT ROUTES
# -------------------------------
@app.get('/view')
def view():
    return load_data()


@app.get('/patient/{patient_id}')
async def view_patient(
    patient_id: str = Path(..., description='Id of the patient in the db', example='P001')
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
    order: str = Query('asc', description='Sort order: asc or desc')
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    data[patient.id] = patient.model_dump()
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient Updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted'})
#