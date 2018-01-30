# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from crawler.models import Article
#
#
# class PostFetcherPipeline(object):
#     def process_item(self, item, spider):
#         article = Article()
#         article.title = item['title']
#         article.link = item['link']
#         article.timestamp = item['timestamp']
#         article.save()
#         return article

class PostFetcherPipeline(object):
    def process_item(self, item, spider):
        if item:
            item.save()
