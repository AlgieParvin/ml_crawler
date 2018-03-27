from datetime import datetime, timedelta

from core.sites import PERIODS
from core.models import Article


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

    month_start = today - timedelta(days=today.day-1)
    month_start = datetime(year=month_start.year, month=month_start.month, day=month_start.day)
    month_count = Article.objects.filter(site__name=site_name, timestamp__gte=month_start).count()

    return tuple(zip(PERIODS, (all_count, today_count, yesterday_count, week_count, month_count)))
