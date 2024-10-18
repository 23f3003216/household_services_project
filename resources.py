from flask_login import current_user
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from models import Service, ServiceRequest, db, Customer, ServiceProfessional
from flask_security import auth_required
from flask import request


parser = reqparse.RequestParser()
parser.add_argument('service_id', type=int, help="Service ID is required", required=True)

parser.add_argument('professional_id', type=int, help="Professional ID should be an integer")
parser.add_argument('remarks', type=str, help="Remarks should be a string")

service_request_fields = {
    'id': fields.Integer,
    'service_id': fields.Integer,
    'customer_id': fields.Integer,
    'professional_id': fields.Integer,
    'date_of_request': fields.DateTime,
    'date_of_completion': fields.DateTime,
    'service_status': fields.String,
    'remarks': fields.String,
}

package_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'description': fields.String,
    'time_required': fields.String,
    'phone': fields.String,
    'experience': fields.Integer,
    'address': fields.String,
    'pincode': fields.String,
}


class ServiceRequestResource(Resource):


    @auth_required('token', 'session')
    @marshal_with(service_request_fields)
    def get(self):
        all_requests = ServiceRequest.query.all()
        return all_requests

    @auth_required('token', 'session')
    def post(self):
        args = parser.parse_args()
        service_id = args['service_id']
        customer_id = current_user.id
        professional_id = args.get('professional_id')
        remarks = args.get('remarks')
        if not professional_id:
            return {"message": "Service Professional is required"}, 400

        professional = ServiceProfessional.query.get(professional_id)
        if not professional:
            return {"message": "Service Professional not found"}, 404


        new_service_request = ServiceRequest(
            service_id=service_id,
            customer_id=customer_id,
            professional_id=professional_id,
            remarks=remarks,
            service_status='requested'
        )

        db.session.add(new_service_request)
        db.session.commit()
        return {"message": "Service request created successfully"}, 201
    @auth_required('token', 'session')
    def patch(self, request_id):
        # Accept or reject logic based on request_id
        action = request.json.get('action')
        request_to_update = ServiceRequest.query.get(request_id)
        
        if not request_to_update:
            return {"message": "Request not found"}, 404

        if action == 'accept':
            request_to_update.service_status = 'accepted'
        elif action == 'reject':
            request_to_update.service_status = 'rejected'
        else:
            return {"message": "Invalid action"}, 400
        
        db.session.commit()
        return {"message": "Request status updated successfully"}, 200

service_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'description': fields.String,
    'time_required': fields.String
}

class ServiceResource(Resource):

 
    @marshal_with(service_fields)
    def get(self):
        all_services = Service.query.all()
        return all_services


    @auth_required('token', 'session')
    def post(self):
        data = request.get_json()
        new_service = Service(
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description'),
            time_required=data.get('time_required')
        )
        db.session.add(new_service)
        db.session.commit()
        return {"message": "Service added successfully"}, 201
    
    
    
class ServicePackagesResource(Resource):
    @marshal_with(package_fields)
    def get(self, service_id):
        service_professionals = ServiceProfessional.query.filter_by(service_type=service_id).all()
        return service_professionals
    
class ServiceHistoryResource(Resource):
    @auth_required('token', 'session')
    def get(self):
        customer_id = current_user.id
        service_history = db.session.query(
            ServiceRequest.id,
            Service.name.label("service_name"),
            ServiceProfessional.name.label("professional_name"),
            ServiceProfessional.phone,
            ServiceRequest.service_status
        ).join(Service, Service.id == ServiceRequest.service_id) \
         .join(ServiceProfessional, ServiceProfessional.id == ServiceRequest.professional_id) \
         .filter(ServiceRequest.customer_id == customer_id).all()

        history_list = []
        for history in service_history:
            history_list.append({
                "id": history.id,
                "service_name": history.service_name,
                "professional_name": history.professional_name,
                "phone": history.phone,
                "status": history.service_status
            })
        
        return {"service_history": history_list}, 200



api = Api()

api.add_resource(ServiceRequestResource, '/api/service-requests')
api.add_resource(ServiceResource, '/api/services')
api.add_resource(ServicePackagesResource, '/api/service-packages/<int:service_id>')
api.add_resource(ServiceHistoryResource, '/api/service-history')
