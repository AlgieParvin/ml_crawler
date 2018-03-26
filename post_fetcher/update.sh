#!/usr/bin/env bash
cd /home/ExoticButters/ml_crawler/post_fetcher;
source ../venv/bin/activate;
scrapy crawl reddit;
scrapy crawl machine_learning_mastery;
scrapy crawl machine_learning_weekly;
scrapy crawl mit_news;
