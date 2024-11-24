from functools import cache
from flask_caching import Cache
from flask import app, flash, redirect, render_template, render_template_string, Flask, request, jsonify, url_for
from flask_login import login_user
from flask_security import auth_required, current_user, roles_required, roles_accepted, SQLAlchemyUserDatastore
from flask_security.utils import hash_password, verify_password
from werkzeug.utils import secure_filename
from extensions import db, security
from datetime import datetime
import os
from models import Customer, Service, ServiceProfessional,Role,User,UserRoles
cache = cache
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_views(app: Flask, user_datastore,cache):
    @app.get('/cache')
    @cache.cached(timeout=5)
    def cache_view():
        return {'time': str(datetime.now())}
    
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
        
    @app.route('/user-login', methods=['POST'])
    def user_login():
      data = request.get_json()
      email = data.get('email')
      password = data.get('password')
      if not email or not password:
        return jsonify({'message': 'Email or password not provided'}), 400

      user = User.query.filter_by(email=email).first()

      if not user:
        return jsonify({'message': 'Invalid user'}), 400

      if verify_password(password, user.password):
        login_user(user)  
        professional_id = None
        if user.roles and user.roles[0].name == 'service_professional':
            professional_profile = ServiceProfessional.query.filter_by(user_id=user.id).first()
            if professional_profile:
                professional_id = professional_profile.id  # Adjust field name if needed

        # Return the response, include professional_id only for service professionals
        response = {
            'token': user.get_auth_token(),
            'user': user.email,
            'role': user.roles[0].name if user.roles else None
        }

        if professional_id:  # Only include professional_id if the user is a service professional
            response['professional_id'] = professional_id

        return jsonify(response), 200
      else:
        return jsonify({'message': 'Invalid password'}), 400

        

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
        service_type_name = data.get('service_type')
        experience = data.get('experience')
        service = Service.query.filter_by(name=service_type_name).first()
        if service is None:
                return jsonify({'message': 'Service not found'}), 404

        if 'documents' not in request.files:
            return jsonify({'message': 'Document upload is required'}), 400

        file = request.files['documents']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create a professional profile
        professional_profile = ServiceProfessional(
            name=name,
            service_type=service.id,
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
    




