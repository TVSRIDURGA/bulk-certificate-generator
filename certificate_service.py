from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from database import SessionLocal
import models


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    certificate_id: int,
    recipient_name: str,
    event_name: str
):
    file_path = OUTPUT_DIR / f"certificate_{certificate_id}.pdf"

    pdf = canvas.Canvas(str(file_path), pagesize=A4)

    width, height = A4

    # Title
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 150,
        "CERTIFICATE OF COMPLETION"
    )

    # Recipient text
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 230,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(
        width / 2,
        height - 280,
        recipient_name
    )

    # Event
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 340,
        f"for successfully completing {event_name}"
    )

    # Save PDF
    pdf.save()

    return str(file_path)


def process_job(db, job):
    successful = 0
    failed = 0

    job.status = "PROCESSING"
    db.commit()

    for certificate in job.certificates:
        try:
            certificate.status = "PROCESSING"
            db.commit()

            file_path = generate_certificate(
                certificate.id,
                certificate.recipient_name,
                job.event_name
            )

            certificate.file_path = file_path
            certificate.status = "SUCCESS"
            successful += 1

        except Exception as e:
            certificate.status = "FAILED"
            certificate.error_message = str(e)
            failed += 1

        db.commit()

    job.successful = successful
    job.failed = failed

    if failed == 0:
        job.status = "COMPLETED"
    elif successful == 0:
        job.status = "FAILED"
    else:
        job.status = "PARTIALLY_COMPLETED"

    db.commit()


def process_job_in_background(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(models.GenerationJob).filter(
            models.GenerationJob.id == job_id
        ).first()

        if job is not None:
            process_job(db, job)

    finally:
        db.close()