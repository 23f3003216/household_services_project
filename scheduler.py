from celery import Celery
from celery.schedules import crontab
from tasks import send_daily_reminders

celery = Celery()

celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=18, minute=0),  
    },
    'send-monthly-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),  
    },
}

celery.conf.timezone = 'UTC'
