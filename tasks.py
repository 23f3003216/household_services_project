from celery_config import celery
from models import ServiceProfessional, ServiceRequest
from flask import Flask

app = Flask(__name__)

@celery.task
def send_daily_reminders():
    with app.app_context():
        professionals = ServiceProfessional.query.all()
        for professional in professionals:
            pending_requests = ServiceRequest.query.filter_by(professional_id=professional.id, service_status='requested').all()
            if pending_requests:
                # Send reminder
                message = f"Hello {professional.name}, you have pending service requests. Please visit the app to accept/reject them."
                send_reminder(professional, message)

def send_reminder(professional, message):
    # Replace this with your preferred method (Google Chat Webhooks, SMS, email, etc.)
    print(f"Sending reminder to {professional.name}: {message}")
