# views.py
from flask import render_template, render_template_string, Flask, request, jsonify
from flask_security import auth_required, current_user, roles_required
from flask_security.utils import hash_password
from werkzeug.utils import secure_filename
from extensions import db, security
import os

from models import Customer, ServiceProfessional

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_views(app: Flask, user_datastore):
    
    @app.route('/')
    def home():
        return render_template('index.html') 

    @app.route('/profile')
    @auth_required('token', 'session')
    def profile():
        return render_template_string(
            """
                <h1>Your Profile</h1>
                <p>Welcome, {{ current_user.email }}</p>
                <p>Role: {{ current_user.roles[0].description }}</p>
                <p><a href="/logout">Logout</a></p>
            """
        )

    @app.route('/register', methods=['POST'])
    def register():
        data = request.form
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        name = data.get('name')
        address = data.get('address')
        pincode = data.get('pincode')

        if not email or not password or not role or not name or not address or not pincode:
            return jsonify({'message': 'Invalid input'}), 403

        if user_datastore.find_user(email=email):
            return jsonify({'message': 'User already exists'}), 400

        if role == 'service_professional':
            service_type = data.get('service_type')
            experience = data.get('experience')

            if 'documents' not in request.files:
                return jsonify({'message': 'Document upload is required'}), 400

            file = request.files['documents']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            user = user_datastore.create_user(email=email, password=hash_password(password), active=True, roles=['service_professional'])
            professional_profile = ServiceProfessional(
                name=name,
                service_type=service_type,
                experience=experience,
                address=address,
                pincode=pincode,
                documents=filename,  
                user_id=user.id
            )
            db.session.add(professional_profile)
            db.session.commit()
            return jsonify({'message': 'Service professional successfully registered'}), 201

        elif role == 'customer':
            user = user_datastore.create_user(email=email, password=hash_password(password), active=True, roles=['customer'])
            customer_profile = Customer(
                name=name,
                address=address,
                pincode=pincode,
                user_id=user.id
            )
            db.session.add(customer_profile)
            db.session.commit()
            return jsonify({'message': 'Customer successfully registered'}), 201

        return jsonify({'message': 'Invalid role'}), 400

    @app.route('/admin-dashboard')
    @roles_required('admin')
    def admin_dashboard():
        return render_template_string(
            """
                <h1>Admin Dashboard</h1>
                <p>This page is only accessible to admins.</p>
                <p><a href="/manage-users">Manage Users</a></p>
                <p><a href="/logout">Logout</a></p>
            """
        )
    
    @app.route('/service-dashboard')
    @roles_required('service_professional')
    def service_dashboard():
        return render_template_string(
            """
                <h1>Service Professional Dashboard</h1>
                <p>This page is only accessible to service professionals.</p>
                <p><a href="/view-jobs">View Assigned Jobs</a></p>
                <p><a href="/logout">Logout</a></p>
            """
        )

    @app.route('/customer-dashboard')
    @roles_required('customer')
    def customer_dashboard():
        return render_template_string(
            """
                <h1>Customer Dashboard</h1>
                <p>This page is only accessible to customers.</p>
                <p><a href="/book-service">Book a Service</a></p>
                <p><a href="/logout">Logout</a></p>
            """
        )

    @app.route('/services')
    def services():
        return render_template_string(
            """
                <h1>Our Services</h1>
                <ul>
                    <li>Plumbing - $100</li>
                    <li>AC Servicing - $150</li>
                    <li>Electrician - $120</li>
                </ul>
                <p><a href="/book-service">Book a Service</a></p>
            """
        )

    @app.route('/book-service')
    @roles_required('customer')
    def book_service():
        return render_template_string(
            """
                <h1>Book a Service</h1>
                <p>Select the service you want to book.</p>
                <p><a href="/services">View Services</a></p>
                <p><a href="/logout">Logout</a></p>
            """
        )

