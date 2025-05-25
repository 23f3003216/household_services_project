Project Statement: Household Services Application

It is a multi-user app ( one admin, service professionals and customers) which acts as a platform for
providing comprehensive home servicing and solutions.

Approach:
● The application was developed with a comprehensive approach to user registration,
authentication, and role-based functionalities. Separate registration forms were designed for
service professionals and customers, while a unified login form was created for all users,
including admin, service professionals, and customers. Role-Based Access Control (RBAC) and
Flask-Login were implemented to ensure proper authentication and user differentiation.

● Key models, such as User, Service, ServiceRequest, ServiceProfessional, and Customer, were
defined, with relationships and back references established using SQLAlchemy to manage
connections between users, services, and requests. An admin dashboard was created to facilitate
user management, including flagging or reinstating users, and service management, where
admins can create, update, or delete services and set base prices.

● Service professionals were equipped with functionality to manage service requests assigned to
them, while customers could search for services by name or location, create new service
requests, edit existing ones, and close them. Backend jobs were automated using Celery,
including daily reminders for pending requests, monthly activity reports for customers, and
user-triggered CSV exports of closed service requests, with alerts sent upon completion.

● To enhance performance, Redis was used for caching, with cache expiry configured to maintain
data freshness.

Frameworks and Libraries Used:
● Flask
● SQLAlchemy
● VueJS for UI
● WTForms
● Flask-restful API
● Flask-WTF
● Flask-Login
● Redis for caching
● Redis and Celery for batch jobs
● Flask-Migrate

API End Points:
/api/service-requests
● GET: Fetch all service requests (cached for 60 seconds).

● POST: Create a new service request (requires service_id, professional_id, remarks
[optional]).

● PATCH: Update the status of a specific service request (accept or reject).
/api/services

● GET: Fetch all available services (cached for 60 seconds).

● POST: Add a new service (requires name, price, description, time_required).

● PUT: Update an existing service by ID (requires service_id, and fields to update: name,
price, description, time_required).

● DELETE: Delete a service by ID (requires service_id).
/api/services/<int:service_id>

● Handles service-specific actions like updating or deleting a service by its ID.
/api/service-packages/<int:service_id>

● GET: Fetch all service professionals for a specific service type (filtered by service_id).
/api/service-history

● GET: Fetch the service history for the current logged-in customer (includes service name,
professional name and phone, service status).
/api/service-requests/professional/<int:professional_id>

● GET: Fetch all service requests assigned to a specific professional (professional_id).
/api/all-users

● GET: Fetch a list of all users (includes id, email, active status, and assigned roles).
/api/users/<int:user_id>/<string:action>

● PUT: Block or unblock a user by their ID (action: either block or unblock).

Drive link of the presentation video:
https://drive.google.com/file/d/1C9qkvucZGc1pTp6lDcyPxJChmTJQi2ci/view?usp=sharing
