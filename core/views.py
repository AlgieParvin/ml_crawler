from datetime import datetime, timedelta

from django.http import Http404
from django.shortcuts import render

from core.models import Article, Site


def machine_learning_mastery(request, period='all'):
    return get_articles(request, 'Machine Learning Mastery', period)


def reddit(request, period='all'):
    return get_articles(request, 'reddit', period)


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


def get_articles(request, site_name, period='all'):
    articles = load_articles(site_name, period)
    sites = Site.objects.all()
    current_site = Site.objects.get(name=site_name)
    periods = ['all', 'today', 'yesterday', 'week', 'month']
    context = {'articles': articles, 'sites': sites,
               'current_site': current_site, 'periods': periods,
               'period': period}
    return render(request, 'core/articles.html', context)
