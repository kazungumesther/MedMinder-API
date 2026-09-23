# 💊 Med-Minder API

A production-ready, clean-architecture backend engine for a medicine reminder and adherence tracking application. Built using **FastAPI**, **SQLAlchemy ORM (v2.0)**, and **PostgreSQL**.

##  Architectural Design & Patterns

This project intentionally rejects basic flat code structures in favor of an enterprise-grade **Layered Architecture** paired with the **Repository Pattern**. This decoupling guarantees high maintainability, strict separation of concerns, and clean testing boundaries.

### Core Separation of Layers:
*   **`app/models/` (Data Layer):** Handles declarative SQLAlchemy blueprints mapping properties safely to physical PostgreSQL tables.
*   **`app/schemas/` (Validation Layer):** Uses Pydantic data validation models to act as an incoming/outgoing JSON gateway shield.
*   **`app/repositories/` (Storage Layer):** Encapsulates raw SQL transactions and ORM data queries away from the business loop.
*   **`app/services/` (Business Logic Layer):** Houses central multi-entity data rules, such as automatic pill stock deduction upon dose completion.
*   **`app/routers/` (Interface Layer):** Exposes RESTful HTTP routing pathways utilizing dependency injections (`get_db`).

---

## 🛠️ Tech Stack & Key Features

*   **Backend Framework:** FastAPI (Asynchronous Python)
*   **Database ORM:** SQLAlchemy 2.0 with custom Connection Pooling (`pool_size=10`, `max_overflow=20`)
*   **Data Integrity:** Fully enforced PostgreSQL constraints (Foreign keys, UUID primary keys, and strict enum check-constraints)
*   **Automated Seed Pipeline:** Standalone data simulation tracker scripts to rapidly populate local instances with valid historical data profiles.

---

##  Technical Highlights for Interviewers

### 1. Advanced Cross-Entity Business Logic
When an adherence status log is recorded as `"taken"`, the system triggers an execution intercept inside `AdherenceService`. It fetches the corresponding medication asset table and **automatically decrements the `stock_quantity` inventory tracking index by 1**. This demonstrates dynamic data handling across model boundaries.

### 2. Defensive Data Ingestion
All API routes utilize strict Pydantic parsing filters to intercept bad user requests (e.g., negative stock allocations or malformed timestamps) before they strike connection resources or trigger database engine exceptions.

---

## 🏁 Quickstart & Execution

### 1. Local Package Assembly
Clone the repository and set up your virtual workspace:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Auto-Populating Test Datasets (Developer Experience)
Satisfy table relationships, foreign key constraints, and seed realistic data records into your database instantly with a single command:
```bash
PYTHONPATH=. python3 seed.py
```

### 3. Launching the Gateway Server
Boot up the engine and access the interactive documentation suite:
```bash
PYTHONPATH=. python3 -m uvicorn app.main:app --reload
```
 **Interactive Documentation Board URL:** `http://127.0.0`
