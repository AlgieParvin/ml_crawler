import csv

from core.django_setup import django_setup
django_setup()

from core.models import Article, Site
from core.sites import ML_MASTERY, ML_WEEKLY, REDDIT, MIT_NEWS


def load_to_db_from_csv(file):
    sites_names = (REDDIT, ML_MASTERY, ML_WEEKLY, MIT_NEWS)
    sites = [Site.objects.get(name=site) for site in sites_names]
    sites_dict = dict(zip(sites_names, sites))

    with open(file, 'r') as f:
        reader = csv.reader(f)
        articles = [
            Article(title=row[0], link=row[1], timestamp=row[2], site=sites_dict[row[3]])
            for row in reader
        ]
        Article.objects.bulk_create(articles)


if __name__ == '__main__':
    load_to_db_from_csv('core.csv')
