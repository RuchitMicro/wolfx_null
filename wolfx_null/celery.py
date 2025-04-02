# celery.py

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wolfx_null.settings')

# Create a new Celery app instance.
app = Celery('wolfx_null')

# Load the configuration from Django settings, using the CELERY namespace.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in your Django app configs.
app.autodiscover_tasks()

# To run the Celery worker, use:
# celery -A wolfx_null worker -l info
# To run the Celery beat scheduler, use:
# celery -A wolfx_null beat -l info

# Optional: Define a debug task to ensure Celery is working.
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

    
