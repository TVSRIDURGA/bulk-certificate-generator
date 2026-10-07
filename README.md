
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

## Architecture


Client
   |
   | POST /api/jobs
   v
FastAPI API
   |
   +--------------------+
   |                    |
   v                    v
Pydantic Validation   SQLite Database
   |                    |
   +---------+----------+
             |
             v
      Background Task
             |
             v
    Certificate Generator
             |
             v
        ReportLab
             |
             v
      Generated PDF Files
             |
             v
      Job Status Tracking


## Processing Flow
1. The client sends a single bulk request containing the event name and recipient details.
2. FastAPI validates the request using Pydantic.
3. A generation job is created and stored in the database.
4. A certificate record is created for each recipient.
5. The job is submitted to a FastAPI background task.
6. Each certificate is processed independently.
7. ReportLab generates a PDF certificate for each successful recipient.
8. Certificate status and file path are stored in the database.
9. The job maintains successful and failed certificate counts.
10. The client can check the job status and retrieve generated certificates.


## How the System Works
1. Create a Generation Job
The client sends a single request containing:
- Event name
- List of recipients
- Recipient names
- Recipient email addresses
The API validates the input and creates a generation job in the database.
Each recipient is also stored as an individual certificate record.
The job initially has the status:
PENDING

2. Background Processing
After creating the job, certificate generation is started as a FastAPI background task.
The job status changes to:
PROCESSING

Each certificate is processed independently.
For every recipient:
Recipient
   ↓
Generate PDF
   ↓
Save PDF
   ↓
Update certificate status


3. Certificate Generation
ReportLab is used to generate the PDF certificate.
The generated certificate contains:
- Certificate title
- Recipient name
- Event name
The generated file is stored in the generated_certificates directory.
4. Failure Handling
Each certificate is processed inside its own error-handling block.
If one certificate fails:
Recipient 1 → SUCCESS
Recipient 2 → FAILED
Recipient 3 → SUCCESS

the other certificates continue processing.
The final job status becomes:
PARTIALLY_COMPLETED

This prevents a single certificate failure from unnecessarily stopping the entire bulk operation.

##Job Statuses

Status	                    Meaning
PENDING	                    Job has been created but processing has not started
PROCESSING	                Certificates are currently being generated
COMPLETED	                All certificates were generated successfully
PARTIALLY_COMPLETED	        Some certificates succeeded and some failed
FAILED	                    All certificate generations failed


API Endpoints
1. Create Generation Job
POST /api/jobs
Example request:
{
  "event_name": "Python Workshop",
  "recipients": [
    {
      "name": "Durga",
      "email": "durga@example.com"
    },
    {
      "name": "Rahul",
      "email": "rahul@example.com"
    }
  ]
}

![Screenshot]("C:\Users\tvsri\OneDrive\Pictures\Screenshots\Screenshot 2026-10-07 214300.png")



