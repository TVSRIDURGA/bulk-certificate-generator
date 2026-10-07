from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():
    """Test the home endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bulk Certificate Generator API is running"
    }


"""job creation test"""

def test_create_generation_job():
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Python Workshop",
            "recipients": [
                {
                    "name": "Durga Test",
                    "email": "durga.test@example.com"
                },
                {
                    "name": "Rahul Test",
                    "email": "rahul.test@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Generation job created successfully"
    assert data["event_name"] == "Python Workshop"
    assert data["total"] == 2
    assert "job_id" in data

"""validation test"""

def test_invalid_email():
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Python Workshop",
            "recipients": [
                {
                    "name": "Invalid User",
                    "email": "not-an-email"
                }
            ]
        }
    )

    assert response.status_code == 422

"""Test certificate generation"""

def test_certificate_generation():
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Certificate Test",
            "recipients": [
                {
                    "name": "Certificate User",
                    "email": "certificate@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    job_id = data["job_id"]

    # Check the job status
    status_response = client.get(f"/api/jobs/{job_id}")

    assert status_response.status_code == 200

    status_data = status_response.json()

    assert status_data["status"] == "COMPLETED"
    assert status_data["total"] == 1
    assert status_data["successful"] == 1
    assert status_data["failed"] == 0

"""Job Status API Test"""

def test_job_status():
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Status Test",
            "recipients": [
                {
                    "name": "Status User",
                    "email": "status@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    status_response = client.get(f"/api/jobs/{job_id}")

    assert status_response.status_code == 200

    data = status_response.json()

    assert data["job_id"] == job_id
    assert data["event_name"] == "Status Test"
    assert data["total"] == 1
    assert data["successful"] == 1
    assert data["failed"] == 0
    assert data["status"] == "COMPLETED"


"""Certificate Retrieval Test"""
def test_certificate_retrieval():
    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Retrieval Test",
            "recipients": [
                {
                    "name": "Download User",
                    "email": "download@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    # Get the job's certificates directly from the database
    from database import SessionLocal
    import models

    db = SessionLocal()

    try:
        certificate = db.query(models.Certificate).filter(
            models.Certificate.job_id == job_id
        ).first()

        assert certificate is not None
        assert certificate.status == "SUCCESS"

        certificate_id = certificate.id

    finally:
        db.close()

    # Retrieve the generated certificate
    download_response = client.get(
        f"/api/certificates/{certificate_id}"
    )

    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/pdf"


"""Add the individual failure test"""

def test_individual_certificate_failure(monkeypatch):
    import certificate_service

    def fake_generate_certificate(
        certificate_id,
        recipient_name,
        event_name
    ):
        if recipient_name == "Fail User":
            raise Exception("Simulated certificate generation failure")

        return "generated_certificates/test_success.pdf"

    monkeypatch.setattr(
        certificate_service,
        "generate_certificate",
        fake_generate_certificate
    )

    response = client.post(
        "/api/jobs",
        json={
            "event_name": "Failure Test",
            "recipients": [
                {
                    "name": "Success User",
                    "email": "success@example.com"
                },
                {
                    "name": "Fail User",
                    "email": "fail@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    status_response = client.get(
        f"/api/jobs/{job_id}"
    )

    assert status_response.status_code == 200

    data = status_response.json()

    assert data["status"] == "PARTIALLY_COMPLETED"
    assert data["total"] == 2
    assert data["successful"] == 1
    assert data["failed"] == 1
