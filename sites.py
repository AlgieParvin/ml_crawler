import os
import sys

import django

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ml_crawler.settings'

django.setup()

from core.models import Site

sites = (
    ('reddit', 'reddit.com'),
    ('Machine Learning Mastery', 'machinelearningmastery.com'),
)

for site in sites:
    Site(name=site[0], url=site[1]).save()
