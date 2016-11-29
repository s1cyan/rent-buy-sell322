''' Use this script to populate the datebase for rbs
    Type in: python populate_rbs.py and check the data in the admin site. '''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rbs_app.settings')
import django
django.setup()
from rbs_application models import 
