from datetime import datetime, timedelta
import time

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from core.models import Article, Site
from core.utils import get_time_counters
from .sites import (
    REDDIT, MIT_NEWS, ML_MASTERY, ML_WEEKLY, sites_info,
    ALL, TODAY, YESTERDAY, WEEK, MONTH
)

ARTICLES_PER_PAGE = 20
PAGES_TO_DISPLAY = 10


class ArticleListView(ListView):
    template_name = 'core/base.html'

    def query_articles(self, site_name, period):
        if period == TODAY:
            today = datetime.today().date()
            today = datetime(year=today.year, month=today.month, day=today.day)
            return Article.objects.filter(site__name=site_name, timestamp__gte=today) \
                .order_by('-timestamp').all()
        if period == ALL:
            return Article.objects.filter(site__name=site_name).order_by('-timestamp').all()
        if period == YESTERDAY:
            today = datetime.today()
            today = datetime(year=today.year, month=today.month, day=today.day)
            yesterday = (today - timedelta(days=1)).date()
            return Article.objects \
                .filter(site__name=site_name, timestamp__gte=yesterday, timestamp__lt=today) \
                .order_by('-timestamp').all()
        if period == WEEK:
            today = datetime.today()
            monday = today - timedelta(days=today.weekday())
            start = datetime(year=monday.year, month=monday.month, day=monday.day)
            return Article.objects.filter(site__name=site_name, timestamp__gte=start) \
                .order_by('-timestamp').all()
        if period == MONTH:
            today = datetime.today()
            start = today - timedelta(days=today.day - 1)
            start = datetime(year=start.year, month=start.month, day=start.day)
            return Article.objects.filter(site__name=site_name, timestamp__gte=start) \
                .order_by('-timestamp').all()
        raise Http404('Page not found')

    def get_queryset(self):
        site_name, period = sites_info[0]['name'], ALL
        try:
            site_name = self.kwargs['site']
            period = self.kwargs['period']
        except ValueError:
            pass
        return self.query_articles(site_name, period)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        # to add
        return context


def machine_learning_mastery(request, period=ALL, page=1):
    return get_articles(request, ML_MASTERY, period, page)


def reddit(request, period=ALL, page=1):
    return get_articles(request, REDDIT, period, page)


def machine_learning_weekly(request, period=ALL, page=1):
    return get_articles(request, ML_WEEKLY, period, page)


def mit(request, period=ALL, page=1):
    return get_articles(request, MIT_NEWS, period, page)


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

    timestamp = time.time()
    # add try / catch
    page_index = int(page)

    paginator = Paginator(load_articles(site_name, period), ARTICLES_PER_PAGE)
    articles = paginator.page(page)

    start_page = page_index - (PAGES_TO_DISPLAY - 1) \
        if page_index % PAGES_TO_DISPLAY == 0 \
        else page_index - (page_index % PAGES_TO_DISPLAY) + 1
    end_page = min(start_page + PAGES_TO_DISPLAY - 1, paginator.num_pages)

    pages = list(range(start_page, end_page + 1))
    print('Pagination ready in', time.time() - timestamp, 'sec')

    timestamp = time.time()
    sites = Site.objects.all()
    current_site = Site.objects.get(name=site_name)
    print('Sites are ready in', time.time() - timestamp, 'sec')

    timestamp = time.time()
    articles_counter = get_time_counters(site_name)
    print('Counters are ready in', time.time() - timestamp, 'sec')

    context = {'articles': articles,
               'sites': sites,
               'current_site': current_site,
               'articles_count': len(articles),

               'periods': articles_counter,
               'period': period,

               'page': page_index,
               'pages': pages,
               'next_page_to_scroll': end_page + 1,
               'previous_page_to_scroll': start_page - 1,

               'has_previous_pages': start_page != 1,
               'has_next_pages': end_page < paginator.num_pages,
               'many_pages': paginator.num_pages > 1}

    timestamp = time.time()
    rendered_page = render(request, 'core/base.html', context)
    print('Rendering page in', time.time() - timestamp, 'sec')
    return rendered_page
