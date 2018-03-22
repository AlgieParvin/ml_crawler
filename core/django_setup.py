import os
import sys
import django

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ml_crawler.settings'

django.setup()
