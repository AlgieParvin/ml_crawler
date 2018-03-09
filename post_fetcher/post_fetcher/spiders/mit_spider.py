import scrapy
from dateutil.parser import parse

from core.models import Article, Site
from .utils import CheckTimeMixin
from ..items import ArticleItem


class MITSpider(scrapy.Spider, CheckTimeMixin):

    name = 'mit_news'
    start_urls = [
        'http://news.mit.edu/topic/machine-learning/'
    ]
    site = Site.objects.get(name='MIT News')
    last_timestamp = Article.objects.filter(site=site).order_by('-timestamp')[0].timestamp \
        if Article.objects.filter(site=site) else None

    def get_link(self, link):
        if link.startswith('/'):
            return 'http://news.mit.edu' + link
        return link

    def parse(self, response):
        for article in response.css('li.views-row'):
            title = article.css('h3.title a::text').extract_first()
            link = article.css('h3.title a::attr(href)').extract_first()
            timestamp = article.css('em.date::text').extract_first()
            if title and link and timestamp:
                tm_with_tz = timestamp + ' 00:00:00 UTC+0'
                full_link = self.get_link(link)
                if MITSpider.posted_after(tm_with_tz, MITSpider.last_timestamp):
                    yield ArticleItem(title=title, link=full_link, timestamp=parse(tm_with_tz),
                                      site=MITSpider.site)
                else:
                    return
