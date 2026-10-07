
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

Example response:
{
  "message": "Generation job created successfully",
  "job_id": 1,
  "event_name": "Python Workshop",
  "total": 2,
  "successful": 0,
  "failed": 0,
  "status": "PENDING"
}


2. Get Job Status
GET /api/jobs/{job_id}

Example:
GET /api/jobs/1

Example response:
{
  "job_id": 1,
  "event_name": "Python Workshop",
  "status": "COMPLETED",
  "total": 2,
  "successful": 2,
  "failed": 0
}

3. Retrieve Generated Certificate

GET /api/certificates/{certificate_id}

Example:
GET /api/certificates/1

The API returns the generated certificate as a PDF file.
Running the Project
1. Clone the repository
git clone https://github.com/TVSRIDURGA/bulk-certificate-generator.git
cd bulk-certificate-generator

2. Create a virtual environment
Windows:
python -m venv venv

Activate it:
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Start the server
uvicorn main:app --reload

The API will be available at:
http://127.0.0.1:8000

Interactive Swagger documentation:
http://127.0.0.1:8000/docs

Testing
The project includes automated tests covering:
- API health check
- Bulk job creation
- Invalid email validation
- Certificate generation
- Job status tracking
- Certificate retrieval
- Individual certificate failure handling
Run the tests using:
python -m pytest

Current test result:
7 passed

Design Decisions
Why FastAPI?
FastAPI provides:
- Simple API development
- Automatic request validation using Pydantic
- Interactive Swagger documentation
- Easy background task support
- Good support for building backend services
Why SQLite?
SQLite was selected because this assignment focuses on backend functionality and certificate generation. It provides a simple relational database without requiring an external database server.
For a production deployment, PostgreSQL or another production-grade relational database could be used.
Why BackgroundTasks?
Certificate generation can involve multiple PDF operations, so it is separated from the immediate API response using FastAPI BackgroundTasks.
This allows the API to create the job and return its job ID while processing continues in the background.
For a larger production system, a durable task queue such as Celery or another distributed job-processing system could be considered.
Why Individual Certificate Records?
Each recipient has a separate certificate record.
This allows the system to independently track:
- Certificate status
- Generated file path
- Error message
It also allows one failed certificate to be recorded without stopping successful certificates.
Error Handling
The API handles:
- Invalid email addresses through Pydantic validation
- Non-existent jobs with a 404 response
- Non-existent certificates with a 404 response
- Certificates that are not yet available with a 400 response
- Individual certificate generation failures without stopping the entire job
Future Improvements
Possible improvements for a production version include:
- PostgreSQL instead of SQLite
- Celery or another distributed task queue
- Redis for task coordination or caching
- Authentication and authorization
- Cloud object storage for generated certificates
- Email delivery of certificates
- Retry mechanisms for failed certificates
- More advanced certificate templates
- Monitoring and logging
- Pagination for large job histories
- Deployment using Docker and cloud infrastructure
Learning Outcomes
Through this project, I gained practical experience with:
- FastAPI backend development
- REST API design
- Pydantic validation
- SQLAlchemy ORM
- Relational database design
- Background task processing
- PDF generation
- Error handling
- Automated API testing
- Git and GitHub workflow





