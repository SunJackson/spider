# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import re
from HouseCrawler.Items.item import *
from scrapy.loader import ItemLoader
from scrapy_djangoitem import DjangoItem
from HouseNew.models import ResidentialArea, RAPicture, RANameInfo, RACoordinate
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class TakeFirstData(object):
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value
        return None


class DefaultItemLoader(ItemLoader):
    default_output_processor = TakeFirstData()


def item_to_django(item, item_type):
    load_item = DefaultItemLoader(item=item_type())
    for key in item.fields.keys():
        load_item.add_value(key, item.get(key, ''))
    item = load_item.load_item()
    return item


class Pipeline(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def safe_format_value(self, value):
        try:
            value = '%.05f' % float(value)
            return str(value)
        except Exception:
            pass
        if isinstance(value, dict):
            try:
                value = dict(value)
                return value
            except Exception:
                pass
        if isinstance(value, list):
            try:
                value = value.sort()
                return value
            except Exception:
                pass
        return str(value)

    def check_item(self, item):
        def load_item(item):
            if isinstance(item, ResidentialAreaItem):
                item = item_to_django(item, ResidentialAreaItem)
                django_item = ResidentialArea(**item)

            elif isinstance(item, RAPictureItem):
                item = item_to_django(item, RAPictureItem)
                django_item = RAPicture(**item)

            elif isinstance(item, RANameInfoItem):
                item = item_to_django(item, RANameInfoItem)
                django_item = RANameInfo(**item)

            elif isinstance(item, RACoordinateItem):
                item = item_to_django(item, RACoordinateItem)
                django_item = RACoordinate(**item)

            else:
                return None

            return django_item

        check_item_flag = True
        item = load_item(item)
        # q_object = item.django_model.objects
        # if isinstance(item, ResidentialAreaItem):
        #     try:
        #         res_object = q_object.filter(TGuid=item['TGuid'])
        #     except ObjectDoesNotExist:
        #         res_object = None
        #
        #     if res_object:
        #         check_item_flag = False
        return check_item_flag, item

    def storage_item(self, item):
        print('storage_item')

        item.save()
        logger.debug("storage item: %(item)s",
                     {'item': item})

    def process_item(self, item, spider):

        if item:
            check_item_flag, now_item = self.check_item(item)
            if check_item_flag:
                logger.debug("item: %(item)s change or met first",
                             {'item': now_item})
                self.storage_item(now_item)
            else:
                logger.debug("item: %(item)s UUID existed",
                             {'item': now_item})
        return item
