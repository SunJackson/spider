#!/usr/python3
# -*- coding: utf-8 -*-
from redis import Redis
import json
r = Redis(host='127.0.0.1', port='6379')
headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache",
}
main_url = 'https://www.zhipin.com/common/data/city.json'
cityurl = 'https://www.zhipin.com/job_detail/?query=&scity={}&industry=&position='.format('101280100')

# result.append(Request(url=cityurl,
#                       headers=headers,
#                       method='GET',
#                       meta={
#                           'PageType': 'CityJobs',
#                       }))
main_base = {
    'source_url': main_url,
    'method': 'GET',
    'meta': {
        'PageType': 'GetCitys',
    }}
base_json = json.dumps(main_base, sort_keys=True)
r.sadd('BossSpider', base_json)