from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from schemas import GenerationJobCreate
from certificate_service import process_job_in_background

import models


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Bulk Certificate Generator API is running"}


@app.post("/api/jobs")
def create_generation_job(
    job: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Create the generation job
    new_job = models.GenerationJob(
        event_name=job.event_name,
        status="PENDING",
        total=len(job.recipients)
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # Create a certificate record for each recipient
    for recipient in job.recipients:
        certificate = models.Certificate(
            job_id=new_job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)

    db.commit()

    # Start certificate generation in the background
    background_tasks.add_task(
        process_job_in_background,
        new_job.id
    )

    return {
        "message": "Generation job created successfully",
        "job_id": new_job.id,
        "event_name": new_job.event_name,
        "total": new_job.total,
        "successful": 0,
        "failed": 0,
        "status": "PENDING"
    }


@app.get("/api/jobs/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(models.GenerationJob).filter(
        models.GenerationJob.id == job_id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }


@app.get("/api/certificates/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = db.query(models.Certificate).filter(
        models.Certificate.id == certificate_id
    ).first()

    if certificate is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Certificate is not available"
        )

    return FileResponse(
        certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )