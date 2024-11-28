from celery import Celery, Task
from flask import Flask

class CeleryConfig:
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    timezone = 'Asia/Kolkata'

class FlaskTask(Task):
    def __init__(self, app=None):
        self.app = app

    def __call__(self, *args, **kwargs):
        with self.app.app_context():
            return self.run(*args, **kwargs)

def celery_init_app(app: Flask) -> Celery:
    celery_app = Celery(app.name)
    celery_app.config_from_object(CeleryConfig)
    celery_app.Task = FlaskTask
    celery_app.Task.app = app
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
