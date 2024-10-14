from extensions import db,security
from flask_security import UserMixin, RoleMixin
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy.orm import relationship

fsqla.FsModels.set_db_info(db)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(65), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    customer_profile = db.relationship('Customer', uselist=False, backref='user_profile')
    professional_profile = db.relationship('ServiceProfessional', uselist=False, backref='user_profile')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)  
    pincode = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = relationship('User', backref='customer_profile')

class ServiceProfessional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service_type = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False) 
    pincode = db.Column(db.String(10), nullable=False)    
    documents = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_verified = db.Column(db.Boolean, default=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = relationship('User', backref='service_professional_profile')
    service = db.relationship('Service', backref='professionals', lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    time_required = db.Column(db.Integer, nullable=False) 

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=True) 
    date_of_request = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(50), default='requested')  
    remarks = db.Column(db.String(255), nullable=True)

    service = db.relationship('Service', backref='service_requests', lazy=True)
    customer = db.relationship('Customer', backref='service_requests', lazy=True)





