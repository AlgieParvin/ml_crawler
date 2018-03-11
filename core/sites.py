import os
import sys

import django
from django.db.utils import IntegrityError

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../../../"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'ml_crawler.settings'

django.setup()

from core.models import Site

sites_info = (
    {
        'name': 'reddit',
        'main_url': 'reddit.com',
        'url_to_crawl': 'https://www.reddit.com/r/MachineLearning/new/',
        'domain': 'https://www.reddit.com'
    },
    {
        'name': 'Machine Learning Mastery',
        'main_url': 'machinelearningmastery.com',
        'url_to_crawl': 'https://machinelearningmastery.com/blog',
        'domain': ''
    },
    {
        'name': 'Machine Learning Weekly',
        'main_url': 'mlweekly.com',
        'url_to_crawl': 'http://mlweekly.com/',
        'domain': ''
    },
    {
        'name': 'MIT News',
        'main_url': 'http://news.mit.edu/topic/machine-learning/',
        'url_to_crawl': 'http://news.mit.edu/topic/machine-learning/',
        'domain': 'http://news.mit.edu'
    },
)

for site in sites_info:
    try:
        Site(**site).save()
    except IntegrityError:
        pass

REDDIT = sites_info[0]['name']
ML_MASTERY = sites_info[1]['name']
ML_WEEKLY = sites_info[2]['name']
MIT_NEWS = sites_info[3]['name']
