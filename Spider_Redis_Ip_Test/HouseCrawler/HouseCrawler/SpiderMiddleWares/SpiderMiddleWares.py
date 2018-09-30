#!/usr/python3
# -*- coding: utf-8 -*-
import redis
import threading


class GetBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host='10.30.1.18', port=6379)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        result = list(result)
        responsetext = response.body_as_unicode()
        if response.status == 200 and '系统检测到您正在使用网页抓取工具访问安居客网站' not in responsetext and '访问验证-安居客' not in responsetext:
            self.r.lpush('success:urls', response.url)
        else:
            self.r.lpush('error:urls', response.url)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
