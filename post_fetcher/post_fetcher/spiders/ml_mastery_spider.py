import scrapy

from core.models import Article, Site
from core.sites import ML_MASTERY
from .utils import CheckTimeMixin
from ..items import ArticleItem


class MachineLearningMasterySpider(scrapy.Spider, CheckTimeMixin):

    name = 'machine_learning_mastery'
    site = Site.objects.get(name=ML_MASTERY)
    start_urls = [site.url_to_crawl]
    last_timestamp = Article.objects.filter(site=site).order_by('-timestamp')[0].timestamp \
        if Article.objects.filter(site=site) else None

    def parse(self, response):
        for article in response.css('article.post'):
            title = article.css('h2.entry-title a::text').extract_first()
            link = article.css('h2.entry-title a::attr(href)').extract_first()
            timestamp = article.css('abbr.date::attr(title)').extract_first()
            if not title or not link or not timestamp:
                yield
            if MachineLearningMasterySpider.posted_after(timestamp, MachineLearningMasterySpider.last_timestamp):
                yield ArticleItem(title=title, link=link, timestamp=timestamp,
                                  site=MachineLearningMasterySpider.site)
