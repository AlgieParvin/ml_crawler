from datetime import datetime, timedelta
import time

from selenium import webdriver

from django.test import LiveServerTestCase

from .models import Site, Article
from .sites import sites_info


class ArticlesPeriodTestCase(LiveServerTestCase):
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

        self.webdriver = webdriver.Firefox()

    def test_reddit_today(self):
        """Reddit articles for today really have only today's articles."""
        self.webdriver.get(self.live_server_url + '/reddit/today')
        page = self.webdriver.page_source
        time.sleep(5)
        self.assertIn(
            '<a class="header" href="#" onclick="window.open(\'https://www.reddit.com\')">Reddit 1</a>', page)
        self.assertNotIn(
            '<a class="header" href="#" onclick="window.open(\'https://www.reddit.com\')">Reddit 2</a>', page)
        self.assertNotIn(
            '<a class="header" href="#" onclick="window.open(\'https://www.reddit.com\')">Reddit 3</a>', page)
        self.assertNotIn(
            '<a class="header" href"#" onclick="window.open(\'https://machinelearningmastery.com\')">ML Mastery 1</a>',
            page)

    def test_reddit_yesterday(self):
        """Reddit articles for yesterday really have only yesterday's articles."""
        self.webdriver.get(self.live_server_url + '/reddit/yesterday')
        page = self.webdriver.page_source
        time.sleep(5)
        self.assertNotIn(
            '<a class="header" href="#" onclick="window.open(\'https://www.reddit.com\')">Reddit 1</a>', page)
        self.assertIn(
            '<a class="header" href="#" onclick="window.open(\'https://www.reddit.com\')">Reddit 2</a>', page)
        self.assertNotIn(
            '<a class="header" href="#" onclick="window.open(\'https://www.reddit.com\')">Reddit 3</a>', page)
        self.assertNotIn(
            '<a class="header" href"#" onclick="window.open(\'https://machinelearningmastery.com\')">ML Mastery 1</a>',
            page)

    def test_ml_mastery_today(self):
        """machinelearningmastery.com articles for today really have only today's articles."""
        self.webdriver.get(self.live_server_url + '/ml_mastery/today')
        page = self.webdriver.page_source
        time.sleep(5)
        self.assertNotIn(
            '<a class="header" href="#" onclick="window.open(\'https://machinelearningmastery.com\'>ML Mastery 1</a>',
            page)
        self.assertNotIn(
            '<a class="header" href="#" onclick="window.open(\'https://machinelearningmastery.com\'>ML Mastery 2</a>',
            page)
        self.assertNotIn(
            '<a class="header" href="#" onclick="window.open(\'https://www.reddit.com\'>Reddit 3</a>', page)

    def tearDown(self):
        self.webdriver.quit()
