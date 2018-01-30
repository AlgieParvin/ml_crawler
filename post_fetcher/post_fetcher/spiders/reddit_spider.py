import scrapy

from core.models import Article, Site
from ..items import ArticleItem
from .utils import CheckTimeMixin


class RedditSpider(scrapy.Spider, CheckTimeMixin):

    name = 'reddit'
    start_urls = [
        'https://www.reddit.com/r/MachineLearning/new/'
    ]
    site = Site.objects.get(name='reddit')
    last_timestamp = Article.objects.filter(site=site).order_by('-timestamp')[0].timestamp \
        if Article.objects.filter(site=site) else None

    def get_link(self, link):
        if link.startswith('/r/'):
            return 'https://www.reddit.com' + link
        return link

    def parse(self, response):
        for post in response.css('div.link'):
            title = post.css('a.title.may-blank::text').extract_first()
            link = post.css('a.title.may-blank::attr(href)').extract_first()
            timestamp = post.css('time.live-timestamp::attr(datetime)').extract_first()
            if not title or not link or not timestamp:
                yield

            link = self.get_link(link)
            if not RedditSpider.last_timestamp:
                yield ArticleItem(title=title, link=link, timestamp=timestamp,
                                  site=RedditSpider.site)
            else:
                if self.posted_after(timestamp, RedditSpider.last_timestamp):
                    yield ArticleItem(title=title, link=link, timestamp=timestamp,
                                      site=RedditSpider.site)
