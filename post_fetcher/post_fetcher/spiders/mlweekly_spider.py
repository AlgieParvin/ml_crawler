import scrapy

from core.models import Article, Site
from core.sites import ML_WEEKLY
from .utils import CheckTimeMixin
from ..items import ArticleItem


class MachineLearningWeeklySpider(scrapy.Spider, CheckTimeMixin):

    name = 'machine_learning_weekly'
    site = Site.objects.get(name=ML_WEEKLY)
    start_urls = [site.url_to_crawl]
    last_timestamp = Article.objects.filter(site=site).order_by('-timestamp')[0].timestamp \
        if Article.objects.filter(site=site) else None

    def parse(self, response):
        timestamp = response.css('header.issue__heading time::attr(datetime)').extract_first()
        tm_with_tz = timestamp + ' 00:00:00 UTC+0'
        if MachineLearningWeeklySpider.posted_after(tm_with_tz, MachineLearningWeeklySpider.last_timestamp):
            for article in response.css('.item__title'):
                title = article.css('a::text').extract_first()
                link = article.css('a::attr(href)').extract_first()
                if title and link and timestamp:
                    yield ArticleItem(title=title, link=link, timestamp=timestamp,
                                      site=MachineLearningWeeklySpider.site)
