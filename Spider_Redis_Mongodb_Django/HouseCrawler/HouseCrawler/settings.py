# -*- coding: utf-8 -*-

# Scrapy settings for HouseCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(BASE_DIR), 'HouseCrawler'))
sys.path.append(os.path.join(os.path.dirname(BASE_DIR), 'HouseAdmin'))
sys.path.append(os.path.dirname(BASE_DIR))

os.environ['DJANGO_SETTINGS_MODULE'] = 'HouseAdmin.HouseAdmin.settings'
django.setup()

# PROXY_REDIS = dj_settings.SCRAPY_BASE_REDIS_CLIENT
# PROXYFLAG_REDIS = dj_settings.SCRAPY_BASE_REDIS_CLIENT
# BLOOMFILTER_REDIS = dj_settings.BLOOM_FILTER_REDIS_CLIENT

# BASE_MONGO_CLIENT = dj_settings.BASE_MONGO_CLIENT

BOT_NAME = 'HouseCrawler'

SPIDER_MODULES = ['HouseCrawler.Spiders']
NEWSPIDER_MODULE = 'HouseCrawler.Spiders'
COMMANDS_MODULE = 'HouseCrawler.Commands'
LOG_LEVEL = 'INFO'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'HouseCrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSH.ProjectBaseHandleMiddleware': 102,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSH.OpenningunitBaseHandleMiddleware': 103,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSH.BuildingBaseHandleMiddleware': 104,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSH.HouseBaseHandleMiddleware': 105,
    'HouseCrawler.SpiderMiddleWares.SpiderMiddleWaresSH.GetProjectBaseHandleMiddleware': 101,
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 100
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.RandomUserAgent': 1,
    'HouseCrawler.DownloadMiddleWares.ProxyMiddleWares.ProxyMiddleware': 100,
    'HouseCrawler.DownloadMiddleWares.RetryMiddleWares.RetryMiddleware': 120,
}

RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODES = [400,500,403,404,501,502,503,504,400,408,411,413,302,301,407,303,304,305,306,307]
REDIRECT_ENABLED = False


COOKIES_DEBUG = False

DOWNLOAD_DELAY = 0.1
DOWNLOAD_TIMEOUT = 60
RANDOMIZE_DOWNLOAD_DELAY = True
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': 301,
    # 'HouseCrawler.Extensions.responselog.CrawlerLogger': 300,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'HouseCrawler.Pipelines.PipelinesSH.SHPipeline': 300,
}
REACTOR_THREADPOOL_MAXSIZE = 20
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0


# LOG_LEVEL = 'INFO'
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


USER_AGENTS = ["Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
               "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
               "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
               "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
               "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
               "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
               "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
               "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
               "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
               "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
               ]

REDIS_HOST = '10.30.1.18'
# REDIS_HOST = '10.30.1.101'
REDIS_PORT = 6379
Redis_key = 'ShanghaiCrawler:start_urls:Default'
REDIS_START_URLS_AS_SET = True
