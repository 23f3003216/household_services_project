# views.py
from flask import flash, redirect, render_template, render_template_string, Flask, request, jsonify, url_for
from flask_security import auth_required, current_user, roles_required
from flask_security.utils import hash_password
from werkzeug.utils import secure_filename
from extensions import db, security
import os

from models import Customer, ServiceProfessional,Role,User,UserRoles

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_views(app: Flask, user_datastore):
    
    @app.route('/')
    def home():
        return render_template('index.html') 
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash('File successfully uploaded')
            return redirect(url_for('upload_file'))


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
     email = data.get('email').strip().lower()
     password = data.get('password')
     role_name = data.get('role')
     name = data.get('name')
     address = data.get('address')
     phone = data.get('phone')
     pincode = data.get('pincode')

    # Check for missing fields
     if not email or not password or not role_name or not name or not address or not pincode:
        return jsonify({'message': 'Invalid input'}), 403

    # Check if the user already exists
     if user_datastore.find_user(email=email):
        return jsonify({'message': 'User already exists'}), 400
    
    # Find the role
     role = user_datastore.find_role(role_name)
     if role is None:
         return jsonify({'message': 'Invalid role specified'}), 400
    
    # Create the user
     try:
        user = user_datastore.create_user(email=email, password=hash_password(password), active=True)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
     except Exception as e:
        return jsonify({'message': 'User creation failed: ' + str(e)}), 500
     if user.id is None:
        return jsonify({'message': 'User creation failed, user ID is None'}), 500

    # Handle role-specific logic
     if role_name == 'service_professional':
        service_type = data.get('service_type')
        experience = data.get('experience')

        # Check if documents are provided
        if 'documents' not in request.files:
            return jsonify({'message': 'Document upload is required'}), 400

        file = request.files['documents']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create a professional profile
        professional_profile = ServiceProfessional(
            name=name,
            service_type=service_type,
            experience=experience,
            address=address,
            phone=phone, 
            pincode=pincode,
            documents=filename,
            user_id=user.id
        )
        db.session.add(professional_profile)

     elif role_name == 'customer':
        # Create a customer profile
        customer_profile = Customer(
            name=name,
            address=address,
            phone=phone, 
            pincode=pincode,
            user_id=user.id
        )
        db.session.add(customer_profile)
    

    # Commit to the database
     db.session.commit()

     return jsonify({'message': 'User successfully registered'}), 201



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

