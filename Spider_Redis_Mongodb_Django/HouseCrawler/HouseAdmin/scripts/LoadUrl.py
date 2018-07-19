# coding = utf-8
import json
import redis
import random
from pymongo import MongoClient
import sys

from HouseNew.models import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

r = redis.Redis(host='10.30.1.18', port=6379)
headers = {'Host': 'www.fangdi.com.cn',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
                }

def loadBaseUrl():
    starurl = 'http://www.fangdi.com.cn/moreRegion.asp'
    project_base = {
        'source_url': starurl,
        'headers': headers,
        'meta': {'PageType': 'StartProjectBase'}}
    project_base_json = json.dumps(project_base, sort_keys=True)
    r.sadd('ShanghaiCrawler:start_urls', project_base_json)

def run():
    loadBaseUrl()
if __name__ == "__main__":
    loadBaseUrl()


# r = redis.Redis(host='10.30.1.18', port=6379)
# r = redis.Redis(host='127.0.0.1', port=6379)
#
# starurl = 'http://www.fangdi.com.cn/House.asp?ProjectID=OTk4N3wyMDE3LTEyLTF8NjM=&projectName=%C8%DA%D0%C5%B2%AC%C6%B7%D1%C5%D6%FE&PreSell_ID=19701&Start_ID=19589&bname=%C7%E0%C6%D6%C7%F8%D3%AF%C6%D6%BD%D6%B5%C0%B4%F3%D3%AF%C6%D6%C2%B71500%C5%AA7%BA%C5&Param=MjUwMzg0MTUyNXx8MjAxNy0xMi0xIDExOjM2OjA5fHw3NA==&flag=MQ=='
# project_base = {
#                     'source_url': starurl,
#                     "meta": {
#         "PageType": "HouseBase",
#         "building_no": "d247ce961d5932c9938d8cd244e699b9",
#         "opening_unit_no": "019647",
#         "shprojectuuid": "ebd0322c0e8033d79462d9b47a8873f0"
#     }
# }
# project_base_json = json.dumps(project_base, sort_keys=True)
# r.sadd('ShanghaiCrawler:start_urls', project_base_json)
