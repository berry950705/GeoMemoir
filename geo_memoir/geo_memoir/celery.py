import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geo_memoir.settings')

app = Celery('geo_memoir/user')
app.conf.update(
    BROKER_URL='redis://:@127.0.0.1:6379/1'
)
app.autodiscover_tasks(settings.INSTALLED_APPS)


