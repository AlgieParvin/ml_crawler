from datetime import datetime, timedelta

from django.db import models
from django.http import Http404
from django.template.defaultfilters import slugify

from .sites import ALL, TODAY, YESTERDAY, WEEK, MONTH, PERIODS


class Site(models.Model):
    name = models.CharField(max_length=50, unique=True)
    main_url = models.URLField()
    url_to_crawl = models.URLField()
    domain = models.CharField(max_length=100, default='')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_full_link(self, link):
        if link.startswith('/'):
            return self.domain + link
        else:
            return link


class Article(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField()
    timestamp = models.DateTimeField()
    site = models.ForeignKey(Site, models.CASCADE, default=None)

    def __str__(self):
        return self.title

    @staticmethod
    def query_articles(site_name, period):
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

    @staticmethod
    def articles_counters_for_periods(site_name):
        """
        Returns the quantity of articles for each time period,
        e. g. {'ALL': 93, 'TODAY': 2, 'YESTERDAY': 14, 'WEEK': 23, 'MONTH': 54}
        """
        today = datetime.today().date()
        today = datetime(year=today.year, month=today.month, day=today.day)
        today_count = Article.objects.filter(site__name=site_name, timestamp__gte=today).count()

        all_count = Article.objects.filter(site__name=site_name).count()

        yesterday = (today - timedelta(days=1)).date()
        yesterday_count = Article.objects.filter(
            site__name=site_name, timestamp__gte=yesterday, timestamp__lt=today).count()

        monday = today - timedelta(days=today.weekday())
        week_start = datetime(year=monday.year, month=monday.month, day=monday.day)
        week_count = Article.objects.filter(site__name=site_name, timestamp__gte=week_start).count()

        month_start = today - timedelta(days=today.day - 1)
        month_start = datetime(year=month_start.year, month=month_start.month, day=month_start.day)
        month_count = Article.objects.filter(site__name=site_name, timestamp__gte=month_start).count()

        return tuple(zip(PERIODS, (all_count, today_count, yesterday_count, week_count, month_count)))
