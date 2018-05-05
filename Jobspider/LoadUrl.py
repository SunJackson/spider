#!/usr/python3
# -*- coding: utf-8 -*-
from redis import Redis
import json
r = Redis(host='127.0.0.1', port='6379')
main_url = 'https://www.zhipin.com/common/data/city.json'
cityurl = 'https://www.zhipin.com/job_detail/?query=&scity={}&industry=&position='.format('101280100')

# result.append(Request(url=cityurl,
#                       headers=headers,
#                       method='GET',
#                       meta={
#                           'PageType': 'CityJobs',
#                       }))
main_base = {
    'source_url': cityurl,
    'method': 'GET',
    'meta': {
        'PageType': 'CityJobs',
        'CityCode': '101280100',
        'CityName': '广州'
    }}
base_json = json.dumps(main_base, sort_keys=True)
r.sadd('BossSpider', base_json)