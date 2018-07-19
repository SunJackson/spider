# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import redis
import random

from HouseNew.models import *

r = redis.Redis(host='10.30.1.18', port=6379)

headers = {'Host': 'www.fangdi.com.cn',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
                }

def loadProjectUrl():

    cur = BuildingBaseShanghai.objects.aggregate(
        *[
            {
                "$sort": {
                    "CurTimeStamp": 1}}, {
                '$group': {
                    '_id': "$building_no",
                    'project_name': {'$last': '$project_name'},
                    'project_no': {'$last': '$project_no'},
                    'opening_unit_no': {'$last': '$opening_unit_no'},
                    'building_name': {'$last': '$building_name'},
                    'building_no': {'$last': '$building_no'},
                    'building_url': {'$last': '$building_url'},
                    'building_sts': {'$last': '$building_sts'}
                }}],allowDiskUse=True)
    for item in cur:
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
            r.sadd('ShanghaiCrawler:start_urls', project_base_json)

def run():
    loadProjectUrl()
if __name__ == "__main__":
    run()
