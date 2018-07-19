# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import redis
import random

from pymongo import MongoClient

r = redis.Redis(host='10.30.1.18', port=6379)

headers = {'Host': 'www.fangdi.com.cn',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
                }

client = MongoClient('10.30.1.2', 27017)
mongodb = client['shanghai']
def loadProjectUrl():
    sort_data = [('CurTimeStamp', -1)]
    cur = mongodb['building_base_shanghai'].find(sort=sort_data)
    for item in cur[:1000]:
        if item['building_url'] :
            building_info = {
                'source_url': item['building_url'],
                'meta': {
                    'PageType': 'HouseBase',
                    'project_no': item['project_no'],
                    'project_name': item['project_name'],
                    'opening_unit_no': str(item['opening_unit_no']),
                    'building_no': str(item['building_no'])}}
            project_base_json = json.dumps(building_info, sort_keys=True)
            r.sadd('ShanghaiCrawler', project_base_json)

def run():
    loadProjectUrl()
if __name__ == "__main__":
    run()
