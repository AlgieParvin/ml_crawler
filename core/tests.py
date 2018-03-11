from datetime import datetime, timedelta

from django.http import HttpRequest
from django.test import TestCase

import core.views as views
from .models import Site, Article
from .sites import sites_info


class ArticlesPeriodTestCase(TestCase):
    def setUp(self):
        sites = [Site(**site) for site in sites_info]
        for site in sites:
            site.save()

        data = (
            ('Reddit 1', 'https://www.reddit.com', 0, sites[0]),
            ('Reddit 2', 'https://www.reddit.com', 1, sites[0]),
            ('Reddit 3', 'https://www.reddit.com', 8, sites[0]),
            ('ML Mastery 1', 'https://machinelearningmastery.com', 1, sites[1]),
            ('ML Mastery 2', 'https://machinelearningmastery.com', 3, sites[1]),
        )
        for instance in data:
            timestamp = datetime.now() - timedelta(days=instance[2])
            Article(title=instance[0], link=instance[1], timestamp=timestamp, site=instance[3])\
                .save()

    def test_reddit_today(self):
        """Reddit articles for today really have only today's articles."""
        response = views.reddit(HttpRequest(), 'today')
        html = response.content.decode('utf8')
        self.assertIn('<a class="header" href="https://www.reddit.com">Reddit 1</a>', html)
        self.assertNotIn('<a class="header" href="https://www.reddit.com">Reddit 2</a>', html)
        self.assertNotIn('<a class="header" href="https://www.reddit.com">Reddit 3</a>', html)
        self.assertNotIn(
            '<a class="header" href="https://machinelearningmastery.com">ML Mastery 1</a>', html)

    def test_reddit_yesterday(self):
        """Reddit articles for yesterday really have only yesterday's articles."""
        response = views.reddit(HttpRequest(), 'yesterday')
        html = response.content.decode('utf8')
        self.assertNotIn('<a class="header" href="https://www.reddit.com">Reddit 1</a>', html)
        self.assertIn('<a class="header" href="https://www.reddit.com">Reddit 2</a>', html)
        self.assertNotIn('<a class="header" href="https://www.reddit.com">Reddit 3</a>', html)
        self.assertNotIn(
            '<a class="header" href="https://machinelearningmastery.com">ML Mastery 1</a>', html)

    def test_ml_mastery_today(self):
        """machinelearningmastery.com articles for today really have only today's articles."""
        response = views.reddit(HttpRequest(), 'today')
        html = response.content.decode('utf8')
        self.assertNotIn('<a class="header" href="https://machinelearningmastery.com">ML Mastery 1</a>', html)
        self.assertNotIn('<a class="header" href="https://machinelearningmastery.com">ML Mastery 2</a>', html)
        self.assertNotIn('<a class="header" href="https://www.reddit.com">Reddit 3</a>', html)
