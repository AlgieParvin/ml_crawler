import scrapy

from core.models import Article, Site
from .utils import CheckTimeMixin
from ..items import ArticleItem


class MachineLearningMasterySpider(scrapy.Spider, CheckTimeMixin):

    name = 'machine_learning_mastery'
    start_urls = [
        'https://machinelearningmastery.com/blog'
    ]
    site = Site.objects.get(name='Machine Learning Mastery')
    last_timestamp = Article.objects.filter(site=site).order_by('-timestamp')[0].timestamp \
        if Article.objects.filter(site=site) else None

    def parse(self, response):
        for article in response.css('article.post'):
            title = article.css('h2.entry-title a::text').extract_first(),
            link = article.css('h2.entry-title a::attr(href)').extract_first(),
            timestamp = article.css('abbr.date::attr(title)').extract_first()
            if not title or not link or not timestamp:
                yield

            if not MachineLearningMasterySpider.last_timestamp:
                yield ArticleItem(title=title[0], link=link[0], timestamp=timestamp,
                                  site=MachineLearningMasterySpider.site)
            else:
                if MachineLearningMasterySpider.posted_after(timestamp, MachineLearningMasterySpider.last_timestamp):
                    yield ArticleItem(title=title[0], link=link[0], timestamp=timestamp,
                                      site=MachineLearningMasterySpider.site)

                # next_page = response.css('a.next::attr(href)').extract_first()
                # if next_page:
                #     yield response.follow(next_page, callback=self.parse)
