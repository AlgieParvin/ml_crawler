from datetime import datetime, timedelta

from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator

from core.models import Article, Site


PERIODS = ['all', 'today', 'yesterday', 'week', 'month']
ARTICLES_PER_PAGE = 20
PAGES_TO_DISPLAY = 10


def machine_learning_mastery(request, period=PERIODS[0], page=1):
    return get_articles(request, 'Machine Learning Mastery', period, page)


def reddit(request, period=PERIODS[0], page=1):
    return get_articles(request, 'reddit', period, page)


def machine_learning_weekly(request, period=PERIODS[0], page=1):
    return get_articles(request, 'Machine Learning Weekly', period, page)


def mit(request, period=PERIODS[0], page=1):
    return get_articles(request, 'Mit News', period, page)


def load_articles(site_name, period):
    if period == 'today':
        today = datetime.today().date()
        today = datetime(year=today.year, month=today.month, day=today.day)
        return Article.objects.filter(site__name=site_name, timestamp__gte=today)\
            .order_by('-timestamp').all()
    if period == 'all':
        return Article.objects.filter(site__name=site_name).order_by('-timestamp').all()
    if period == 'yesterday':
        today = datetime.today()
        today = datetime(year=today.year, month=today.month, day=today.day)
        yesterday = (today - timedelta(days=1)).date()
        return Article.objects\
            .filter(site__name=site_name, timestamp__gte=yesterday, timestamp__lt=today) \
            .order_by('-timestamp').all()
    if period == 'week':
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        start = datetime(year=monday.year, month=monday.month, day=monday.day)
        return Article.objects.filter(site__name=site_name, timestamp__gte=start) \
            .order_by('-timestamp').all()
    if period == 'month':
        today = datetime.today()
        start = today - timedelta(days=today.day-1)
        start = datetime(year=start.year, month=start.month, day=start.day)
        return Article.objects.filter(site__name=site_name, timestamp__gte=start) \
            .order_by('-timestamp').all()
    raise Http404('Page not found')


def get_articles(request, site_name, period, page):

    # add try / catch
    page_index = int(page)

    paginator = Paginator(load_articles(site_name, period), ARTICLES_PER_PAGE)
    articles = paginator.page(page)

    start_page = page_index - (PAGES_TO_DISPLAY - 1) \
        if page_index % PAGES_TO_DISPLAY == 0 \
        else page_index - (page_index % PAGES_TO_DISPLAY) + 1
    end_page = min(start_page + PAGES_TO_DISPLAY - 1, paginator.num_pages)

    pages = list(range(start_page, end_page + 1))

    sites = Site.objects.all()
    current_site = Site.objects.get(name=site_name)

    context = {'articles': articles,
               'sites': sites,
               'current_site': current_site,

               'periods': PERIODS,
               'period': period,

               'page': page_index,
               'pages': pages,
               'next_page_to_scroll': end_page + 1,
               'previous_page_to_scroll': start_page - 1,

               'has_previous_pages': start_page != 1,
               'has_next_pages': end_page < paginator.num_pages,
               'no_pagination': paginator.num_pages == 1}
    return render(request, 'core/articles.html', context)
