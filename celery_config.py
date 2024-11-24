from celery import Celery

def make_celery(app_name=__name__):
    redis_url = "redis://localhost:6379/0"
    celery = Celery(app_name, broker=redis_url, backend=redis_url)
    celery.conf.update(broker_connection_retry_on_startup=True)
    return celery

celery = make_celery()
