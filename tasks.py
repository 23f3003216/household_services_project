import time
import datetime
from celery import shared_task
from celery_config import make_celery
from models import ServiceProfessional, ServiceRequest
from flask import Flask, make_response, render_template
from flask_mail import Mail, Message
from io import StringIO
import csv

app = Flask(__name__)
celery = make_celery(app)

# Configure Flask-Mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='your-email@example.com',
    MAIL_PASSWORD='your-email-password'
)
mail = Mail(app)

@shared_task(ignore_result=False)
def add(x, y):
    time.sleep(10)
    return x + y

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

@celery.task
def send_monthly_report():
    with app.app_context():
        customers = ServiceProfessional.query.all()
        for customer in customers:
            total_requested = ServiceRequest.query.filter_by(professional_id=customer.id).count()
            total_closed = ServiceRequest.query.filter_by(professional_id=customer.id, service_status='closed').count()

            # Render HTML template
            report_html = render_template('monthly_report.html', name=customer.name, total_requested=total_requested, total_closed=total_closed)

            # Send the email
            msg = Message(subject="Your Monthly Activity Report",
                          sender="your-email@example.com",
                          recipients=[customer.email],
                          html=report_html)
            mail.send(msg)

@celery.task
def export_service_details():
    with app.app_context():
        services = ServiceRequest.query.filter_by(service_status='closed').all()
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['service_id', 'customer_id', 'professional_id', 'date_of_request', 'remarks'])
        for service in services:
            cw.writerow([service.id, service.customer_id, service.professional_id, service.date_of_request, service.remarks])
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=service_details.csv"
        output.headers["Content-type"] = "text/csv"
        return output
