import os
import django
from django.db.utils import IntegrityError

from .django_setup import django_setup
django_setup()

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


REDDIT = sites_info[0]['name']
ML_MASTERY = sites_info[1]['name']
ML_WEEKLY = sites_info[2]['name']
MIT_NEWS = sites_info[3]['name']

PERIODS = ['all', 'today', 'yesterday', 'week', 'month']
ALL, TODAY, YESTERDAY, WEEK, MONTH = PERIODS

if __name__ == '__main__':
    for site in sites_info:
        try:
            Site(**site).save()
        except IntegrityError:
            pass
