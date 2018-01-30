from datetime import datetime, timedelta
from django.http import HttpRequest
from django.test import TestCase

import core.views as views
from core.models import Site, Article


class ArticlesPeriodTestCase(TestCase):
    def setUp(self):
        reddit = Site(name='reddit', url='reddit.com')
        reddit.save()
        ml_mastery = Site(name='Machine Learning Mastery', url='machinelearningmastery.com')
        ml_mastery.save()

        data = (
            ('Reddit 1', 'https://www.reddit.com', 0, reddit),
            ('Reddit 2', 'https://www.reddit.com', 1, reddit),
            ('Reddit 3', 'https://www.reddit.com', 8, reddit),
            ('ML Mastery 1', 'https://machinelearningmastery.com', 1, ml_mastery),
            ('ML Mastery 2', 'https://machinelearningmastery.com', 3, ml_mastery),
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
