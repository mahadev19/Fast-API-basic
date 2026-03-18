# 🏥 Patient Management System API

A production-ready REST API built using **FastAPI** to manage patient records.
This project demonstrates backend API development with authentication, database integration, rate limiting, logging, monitoring, and CI/CD.

---

## 🚀 Features

* Create, view, update, and delete patient records
* Sort patients by height, weight, or BMI
* Automatic BMI calculation and health classification
* JWT-based authentication and authorization
* Rate limiting on sensitive endpoints
* PostgreSQL database integration with SQLAlchemy
* Database migrations using Alembic
* Structured logging
* Environment variable management
* Prometheus + Grafana monitoring
* CI/CD pipeline using GitHub Actions

---

## 🛠 Tech Stack

* Python 3.10
* FastAPI
* Pydantic v2
* PostgreSQL
* SQLAlchemy
* Alembic
* Uvicorn
* SlowAPI
* Prometheus + Grafana
* Docker
* GitHub Actions

---

## 📂 Project Structure
```
FastAPI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── logger.py
│   └── core/
│       └── settings.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env                  # Never commit this
├── .gitignore
├── alembic.ini
├── conftest.py
├── docker-compose.yml
├── prometheus.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/mahadev19/Fast-API-basic.git
```

### 2. Navigate to project folder
```bash
cd Fast-API-basic
```

### 3. Create virtual environment
```bash
python -m venv myevn
```

### 4. Activate virtual environment

Windows:
```bash
myevn\Scripts\activate
```

Mac/Linux:
```bash
source myevn/bin/activate
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Create `.env` file
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/fastapi_db
ADMIN_USERNAME=yourusername
ADMIN_PASSWORD=yourpassword
SECRET_TOKEN=yoursecrettoken
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
```

### 7. Run database migrations
```bash
alembic upgrade head
```

---

## ▶️ Running the API
```bash
uvicorn app.main:app --reload
```

Server runs at:
```
http://127.0.0.1:8000
```

---

## 📘 API Documentation

FastAPI automatically provides interactive documentation.

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## 📌 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/about` | About the API |
| POST | `/login` | Login and get JWT token |

### Patient Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/view` | View all patients |
| GET | `/patient/{patient_id}` | View single patient |
| GET | `/sort?sort_by=bmi&order=desc` | Sort patients |
| POST | `/create` | Create new patient |
| PUT | `/edit/{patient_id}` | Update patient |
| DELETE | `/delete/{patient_id}` | Delete patient |

### Protected Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/protected` | Protected route (Bearer token) |
| GET | `/patients` | OAuth2 protected route |

---

## 🔐 Authentication

### Login
```bash
POST /login
Content-Type: application/x-www-form-urlencoded

username=yourusername&password=yourpassword
```

Response:
```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

### Access Protected Routes
```bash
GET /protected
Authorization: Bearer your_jwt_token
```

---

## 🧮 BMI Calculation

BMI is automatically calculated using:
```
BMI = weight (kg) / height² (m)
```

| BMI Range | Category |
|-----------|----------|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| ≥ 30 | Obese |

---

## 🗄️ Database

### Setup PostgreSQL
```bash
# Create database
createdb fastapi_db

# Run migrations
alembic upgrade head
```

### Create Migration
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## 🔹 Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `ADMIN_USERNAME` | Admin username |
| `ADMIN_PASSWORD` | Admin password |
| `SECRET_TOKEN` | Bearer token for /protected |
| `JWT_SECRET_KEY` | Secret key for JWT signing |
| `JWT_ALGORITHM` | JWT algorithm (default: HS256) |

> ⚠️ Never commit `.env` to GitHub

---

## 🔹 Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `/` | 5 requests/minute |
| `/login` | 3 requests/minute |
| `/users` | 5 requests/minute |

Response when exceeded:
```json
{
  "detail": "Too many requests"
}
```
Status: `429 Too Many Requests`

---

## 🔹 Logging

Every request and response is logged automatically:
```
2026-03-17 12:00:01 - INFO - Request: GET /view
2026-03-17 12:00:01 - INFO - Response status: 200
2026-03-17 12:00:05 - ERROR - Error occurred: division by zero
```

---

## 🔹 Testing

Tests use SQLite so no PostgreSQL setup is needed:
```bash
pytest tests/ -v
```

### Test Coverage

| Test | Description |
|------|-------------|
| `test_root` | Root endpoint returns 200 |
| `test_about` | About endpoint returns 200 |
| `test_create_patient` | Patient created successfully |
| `test_view_patients` | View all patients |
| `test_invalid_login` | Wrong credentials return 400 |

---

## 📊 Monitoring (Prometheus + Grafana)

### Start monitoring stack
```bash
docker-compose up -d
```

### Access services

| Service | URL | Credentials |
|---------|-----|-------------|
| FastAPI metrics | `http://localhost:8000/metrics` | — |
| Prometheus | `http://localhost:9090` | — |
| Grafana | `http://localhost:3000` | admin / admin |

### Configure Grafana

1. Go to **Settings → Data Sources**
2. Add **Prometheus**
3. Set URL: `http://prometheus:9090`
4. Click **Save & Test**

### Useful Queries
```promql
# Total requests
http_requests_total

# Requests per second
rate(http_requests_total[1m])

# Error tracking
http_responses_total{status="500"}

# Request latency
http_request_duration_seconds
```

---

## 🔄 CI/CD Pipeline

GitHub Actions automatically runs tests on every push to `main`.

### Pipeline Steps
```
Push to main
     ↓
Install dependencies
     ↓
Create .env from secrets
     ↓
Run pytest tests
     ↓
✅ Pass or ❌ Fail
```

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `ADMIN_USERNAME` | Admin username |
| `ADMIN_PASSWORD` | Admin password |
| `SECRET_TOKEN` | Bearer token |
| `JWT_SECRET_KEY` | JWT secret key |

---

## 📜 License

This project is for learning and educational purposes.
