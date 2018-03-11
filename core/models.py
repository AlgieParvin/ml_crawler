from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=50, unique=True)
    main_url = models.URLField()
    url_to_crawl = models.URLField()
    domain = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

    def get_full_link(self, link):
        if link.startswith('/'):
            return self.domain + link


class Article(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField()
    timestamp = models.DateTimeField()
    site = models.ForeignKey(Site, models.CASCADE, default=None)

    def __str__(self):
        return self.title
