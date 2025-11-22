import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

from delivery_app.models import Delivery

print('DELIVERY_COUNT:', Delivery.objects.count())
print('SAMPLE:', list(Delivery.objects.values()[:10]))
