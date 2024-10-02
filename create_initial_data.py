from flask_security import SQLAlchemySessionUserDatastore
from extensions import db
from flask_security.utils import hash_password
from models import User,Role,Service


def create_data(user_datastore : SQLAlchemySessionUserDatastore):
    print("creating roles and users") 


    user_datastore.find_or_create_role(name='admin', description="Administrator")
    user_datastore.find_or_create_role(name='service_professional', description="Service Professional")
    user_datastore.find_or_create_role(name='customer', description="Customer")

    # creating initial data

    if not user_datastore.find_user(email="admin@householdservices.com"):
        user_datastore.create_user(email="admin@householdservices.com", password=hash_password("adminpass"), roles=['admin'])

    if not user_datastore.find_user(email="professional@services.com"):
        user_datastore.create_user(email="professional@services.com", password=hash_password("profpass"), roles=['service_professional'])

    if not user_datastore.find_user(email="customer@services.com"):
        user_datastore.create_user(email="customer@services.com", password=hash_password("customerpass"), roles=['customer'])

    service1 = Service(name="Plumbing", price=100, time_required="1 hour", description="Basic plumbing services")
    service2 = Service(name="AC Servicing", price=150, time_required="1.5 hours", description="Air conditioner servicing")
    service3 = Service(name="Electrician", price=120, time_required="1 hour", description="Electrical services")

    db.session.add(service1)
    db.session.add(service2)
    db.session.add(service3)

    db.session.commit()