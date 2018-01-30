from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField()
    timestamp = models.DateTimeField()
    site = models.ForeignKey(Site, models.CASCADE, default=None)

    def __str__(self):
        return self.title
