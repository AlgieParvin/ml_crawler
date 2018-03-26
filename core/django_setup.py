import os
import sys
import django


def django_setup():
    try:
        # In development environment
        from .django_dir import path
    except ImportError:
        # In production
        path = '/home/ExoticButters/ml_crawler'
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ml_crawler.settings'
    django.setup()
