import os
from flask import Flask
from extensions import db, security
import views
from flask_migrate import Migrate
from create_initial_data import create_data
import resources
from flask_restful import Api
from celery_config import celery, make_celery
from cache_config import init_cache
from tasks import add
celery_app = make_celery(__name__) 
def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'should-not-be-seen'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SECURITY_PASSWORD_SALT'] = 'salty-password'
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['UPLOAD_FOLDER'] = 'E:/Projects/Household Services/Uploaded files'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] ='redis://localhost:6379/1'

    celery.conf.update(app.config)
    cache = init_cache(app)


    db.init_app(app)
    migrate = Migrate(app, db)
    app.cache = cache
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.app_context():
        from models import User, Role
        from flask_security import SQLAlchemyUserDatastore

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app, user_datastore)

        if not app.cli.commands:
            db.create_all()

    # Register the CLI command
    app.cli.add_command(create_data)
    
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = []
    app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True

    views.create_views(app, user_datastore,cache) 
    resources.api.init_app(app)
    celery_app = make_celery(app) 
    app.celery_app = celery_app 



    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
