#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import json
r = redis.Redis(host='10.30.1.18', port='6379')
header = { 'accept': "application/json, text/javascript, */*; q=0.01",
    'x-devtools-emulate-network-conditions-client-id': "5CB00670C9C98DBAA2CFEE9F04E34EA3",
    'x-requested-with': "XMLHttpRequest",
    'referer': "https://www.zhipin.com/",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache"
           }
project_base = {
'source_url':'https://www.zhipin.com/common/data/city.json',
    'headers' : header,
        'meta': {'PageType': 'GetCitys',
                 }}
starturl = json.dumps(project_base, sort_keys=True)
def run():
    r.sadd('Crawler:start_urls', starturl)
if __name__ == "__main__":
    run()
