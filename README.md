# Bulk Certificate Generator API

A backend service built with FastAPI that accepts a bulk list of certificate recipients, generates PDF certificates using a predefined template, tracks generation progress, handles individual failures, and provides an API to retrieve generated certificates.

## Features

- Bulk certificate generation through a single API request
- Recipient data validation
- PDF certificate generation using ReportLab
- Background processing using FastAPI BackgroundTasks
- Job status tracking
- Success and failure counts
- Individual certificate failure handling
- Generated certificate retrieval
- SQLite database using SQLAlchemy
- Automated API tests using Pytest

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- HTTPX
- Uvicorn

## Project Structure

```text
bulk-certificate-generator/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── certificate_service.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── tests/
    └── test_api.py