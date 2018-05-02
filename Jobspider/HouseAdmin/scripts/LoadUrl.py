#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import json
r = redis.Redis(host='10.30.1.18', port='6379')

project_base = {
'source_url':'https://www.zhaopin.com/',
        'meta': {'PageType': 'GetCitys',
                 }}
starturl = json.dumps(project_base, sort_keys=True)
def run():
    r.sadd('Crawler:start_urls', starturl)
if __name__ == "__main__":
    run()
