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
git clone https://github.com/yourusername/patient-management-api.git
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

## 📜 License

This project is for learning and educational purposes.
