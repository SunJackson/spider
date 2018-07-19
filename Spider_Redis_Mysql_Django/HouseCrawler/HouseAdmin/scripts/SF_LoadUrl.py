# -*- coding: utf-8 -*-
import json
import uuid

import redis

REDIS_CACHE = redis.Redis('10.30.1.18')


def post_init(**kwargs):
    page = 1
    resident_area_index = {
        '增城': 80,
        '番禺': 78,
        '南沙': 84,
        '花都': 639,
        '白云': 76,
        '海珠': 74,
        '越秀': 72,
        '荔湾': 71,
        '天河': 73,
        '从化': 79,
        '黄埔': 75,
        '广州周边': 15882
    }
    r = REDIS_CACHE
    key = uuid.uuid1().hex
    for i, (name, num) in enumerate(resident_area_index.items()):
        area_list_id = '{RA}__0_0_0_0_{Page}_0_0_0'.format(RA=num, Page=page)
        area_list_url = 'http://esf.gz.fang.com/housing/{}'.format(
            area_list_id)
        residential_area_base = {
            'source_url': area_list_url,
            'meta': {
                'PageType': 'RAList',
                'RA': name,
                'RANum': num
            }
        }
        print(residential_area_base)
        r.sadd('SFCrawler:start_urls', json.dumps(residential_area_base))
    # r.expire(key, int('86400'))
    return key


if __name__ == '__main__':
    post_init()