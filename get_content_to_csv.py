import csv
import requests
from lxml import html
from dateutil.parser import parse

from core.sites import ML_MASTERY, ML_WEEKLY, MIT_NEWS
from core.django_setup import *


from core.models import Site


def download_page(url, headers=None):
    if not headers:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return html.document_fromstring(response.content)


def get_ml_weekly_articles(page, articles, site):
    timestamp = page.cssselect('header.issue__heading time')[0].get('datetime')
    tm_with_tz = timestamp + ' 00:00:00 UTC+0'
    for article in page.cssselect('.item__title'):
        title = article.cssselect('a')
        link = article.cssselect('a')
        if title and link:
            articles.append((title[0].text, link[0].get('href'), timestamp, site.name))


def get_ml_mastery_articles(page, articles, site):
    for article in page.cssselect('article.post'):
        title = article.cssselect('h2.entry-title a')[0].text
        link = article.cssselect('h2.entry-title a')[0].get('href')
        timestamp = article.cssselect('abbr.date')[0].get('title')
        articles.append((title, link, timestamp, site.name))


def get_mit_news(page, articles, site):
    for article in page.cssselect('.view-news-items li.views-row'):
        title = article.cssselect('h3.title a')[0].text
        link = article.cssselect('h3.title a')[0].get('href')
        timestamp = article.cssselect('em.date')[0].text
        if title and link and timestamp:
            tm_with_tz = parse(timestamp + ' 00:00:00 UTC+0')
            full_link = site.get_full_link(link)
            articles.append((title, full_link, tm_with_tz, site.name))


def save_to_csv(articles, file):
    with open(file, 'w') as f:
        writer = csv.writer(f)
        for article in articles:
            writer.writerow(article)


if __name__ == '__main__':
    ml_mastery = Site.objects.get(name=ML_MASTERY)
    ml_weekly = Site.objects.get(name=ML_WEEKLY)
    mit_news = Site.objects.get(name=MIT_NEWS)

    articles = []

    print('machinelearningmastery.com is started')
    main_page = download_page(ml_mastery.url_to_crawl)
    pages_count = int(main_page.cssselect('a.page-numbers')[-2].text)
    for i in range(pages_count):
        page = download_page(ml_mastery.url_to_crawl + str(i + 1))
        get_ml_mastery_articles(page, articles, ml_mastery)
    print('machinelearningmastery.com is done')

    # mlweekly.com

    print('mlweekly.com is started')
    main_page = download_page(ml_weekly.url_to_crawl)
    issue_number = main_page.cssselect('header.issue__heading h1 a')[0].text
    pages_count = int(issue_number.strip()[1:])
    for i in range(pages_count):
        page = download_page(ml_weekly.url_to_crawl + 'issues/' + str(i + 1))
        get_ml_weekly_articles(page, articles, ml_weekly)
    print('mlweekly.com is done')

    # news.mit.edu/topic/machine-learning

    print('news.mit.edu/topic/machine-learning is started')
    main_page = download_page(mit_news.url_to_crawl)
    last_page_url = mit_news.domain + main_page.cssselect('li.pager-last a')[0].get('href')
    pages_count = int(last_page_url.split('=')[-1]) + 1
    for i in range(pages_count):
        page = download_page(mit_news.url_to_crawl[:-1] + '?page=' + str(i))
        get_mit_news(page, articles, mit_news)
    print('news.mit.edu/topic/machine-learning is done')

    save_to_csv(articles, 'articles.csv')
    print('Saved')
