from celery import Celery
from celery.schedules import crontab
from tasks import send_daily_reminders

celery = Celery()

celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),  # Every day at 6pm
    },
}

celery.conf.timezone = 'UTC'
