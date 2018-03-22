import scrapy

from core.models import Article, Site
from core.sites import REDDIT
from ..items import ArticleItem
from .utils import CheckTimeMixin


class RedditSpider(scrapy.Spider, CheckTimeMixin):

    name = 'reddit'
    site = Site.objects.get(name=REDDIT)
    start_urls = [site.url_to_crawl]
    last_timestamp = Article.objects.filter(site=site).order_by('-timestamp')[0].timestamp \
        if Article.objects.filter(site=site) else None

    def parse(self, response):
        for post in response.css('div.link'):
            title = post.css('a.title.may-blank::text').extract_first()
            link = post.css('a.title.may-blank::attr(href)').extract_first()
            timestamp = post.css('time.live-timestamp::attr(datetime)').extract_first()
            if not link:
                link = post.css('a.title.may-blank::attr(data-outbound-url)').extract_first()

            full_link = RedditSpider.site.get_full_link(link)
            if self.posted_after(timestamp, RedditSpider.last_timestamp):
                yield ArticleItem(title=title, link=full_link, timestamp=timestamp,
                                  site=RedditSpider.site)
            else:
                return
        if self.last_timestamp:
            next_page = response.css('span.next-button a::attr(href)').extract_first()
            yield scrapy.Request(url=next_page, callback=self.parse)
