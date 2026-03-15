# Import required libraries
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import os

# Create FastAPI application
app = FastAPI()

# -------------------------------
# Pydantic Model for Patient Data
# -------------------------------
# This class defines the structure of a patient record
class Patient(BaseModel):

    # Patient ID (Example: P001)
    id: Annotated[str, Field(..., description='Id of the patient', example='P001')]

    # Patient name
    name: Annotated[str, Field(..., description='Name of the patient')]

    # City where patient lives
    city: Annotated[str, Field(..., description='City where the patient is living')]

    # Age validation (must be between 1 and 119)
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]

    # Gender must be one of these values
    gender: Annotated[
        Literal['male', 'female', 'others'],
        Field(..., description="Gender of the patient")
    ]

    # Height in meters
    height: Annotated[float, Field(..., gt=0, description='Height of the Patient in meters')]

    # Weight in kilograms
    weight: Annotated[float, Field(..., gt=0, description='Weight of the Patient in kgs')]

    # -----------------------------------
    # Computed Field → BMI Calculation
    # -----------------------------------
    @computed_field
    @property
    def bmi(self) -> float:
        # BMI Formula: weight / height²
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    # -----------------------------------
    # Computed Field → BMI Category
    # -----------------------------------
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


# -------------------------------------------
# Model used for updating patient information
# -------------------------------------------
# All fields are optional because we may update
# only one field instead of the whole record.
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# -----------------------------------
# File Path Setup
# -----------------------------------
# This ensures the JSON file is stored
# in the same directory as the Python file.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "patients.json")


# -----------------------------------
# Function to Load Data from JSON file
# -----------------------------------
def load_data():

    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        # If file does not exist return empty dictionary
        return {}


# -----------------------------------
# Function to Save Data to JSON file
# -----------------------------------
def save_data(data):

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------
# Basic Routes
# -------------------------

# Root endpoint
@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}


# About endpoint
@app.get("/about")
def about():
    return {'message': 'A Fully Functional API to manage your patient records'}


# -----------------------------------
# View All Patients
# -----------------------------------
@app.get('/view')
def view():

    data = load_data()
    return data


# -----------------------------------
# View Single Patient using Patient ID
# -----------------------------------
@app.get('/patient/{patient_id}')
def view_patient(
    patient_id: str = Path(..., description='Id of the patient in the db', example='P001')
):

    data = load_data()

    # Check if patient exists
    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")


# -----------------------------------
# Sort Patients
# -----------------------------------
@app.get('/sort')
def sort_patients(

    sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
    order: str = Query('asc', description='Sort order: asc or desc')
):

    valid_fields = ['height', 'weight', 'bmi']

    # Validate field
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')

    # Validate order
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()

    # Reverse sorting if desc
    sort_order = True if order == 'desc' else False

    # Sort patients
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )

    return sorted_data


# -----------------------------------
# Create New Patient
# -----------------------------------
@app.post('/create')
def create_patient(patient: Patient):

    # Load existing data
    data = load_data()

    # Check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # Add patient to database
    data[patient.id] = patient.model_dump()

    # Save updated data
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={'message': 'Patient created successfully'}
    )


# -----------------------------------
# Update Patient
# -----------------------------------
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    existing_patient_info = data[patient_id]

    # Get only updated fields
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    # Update values
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # Ensure ID remains same
    existing_patient_info['id'] = patient_id

    # Revalidate using Pydantic
    patient_pydantic_obj = Patient(**existing_patient_info)

    # Convert back to dictionary
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'Patient Updated'}
    )


# -----------------------------------
# Delete Patient
# -----------------------------------
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'Patient deleted'}
    )