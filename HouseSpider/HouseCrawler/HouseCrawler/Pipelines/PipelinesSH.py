#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import datetime
from scrapy.loader import ItemLoader
from scrapy.exceptions import DropItem
from pymongo import MongoClient
from HouseCrawler.Items.Item import *

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

logger = logging.getLogger(__name__)


class TakeFirstData(object):
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value
        return ''


class DefaultItemLoader(ItemLoader):
    default_output_processor = TakeFirstData()


class SHPipeline(object):

    def __init__(self, settings):
        self.settings = settings
        client = MongoClient(settings.get('MONGODB_HOST', '127.0.0.1'), 27017)
        self.mongodb = client[settings.get('MONGODB_NAME')]

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

    def find_latest_one(self, table_name, query):
        sort_data = [('CurTimeStamp', -1)]
        cursor = self.mongodb[table_name].find_one(query, sort=sort_data)
        return cursor

    def find_latest_one_update(self, table_name, query, update):
        sort_data = [('CurTimeStamp', -1)]
        self.mongodb[table_name].find_one_and_update(query, update=update, sort=sort_data)

    def check_item(self, item):
        def check_item_change(fillter_item, item):
            monitor_keys = {'house_sts'}
            copy_keys = {'house_class', 'house_use_type', 'house_layout', 'house_area_pr_yc',
                         'house_area_pr_tn', 'house_area_pr_ft', 'house_area_pr_dx', 'house_area_real_tn',
                         'house_area_real_ft', 'house_area_real_dx'}
            diff_flag = False
            for key in item.keys():
                if key not in fillter_item.keys():
                    diff_flag = True
                    break
                if self.safe_format_value(item.get(key)) != self.safe_format_value(fillter_item.get(key)):
                    diff_flag = True

            if isinstance(item, HouseItem) and diff_flag:
                for key in monitor_keys:
                    item[key + 'Latest'] = fillter_item.get(key)
                    if self.safe_format_value(item.get(key)) != self.safe_format_value(fillter_item.get(key)):
                        for copy_key in copy_keys:
                            if self.safe_format_value(fillter_item.get(copy_key)) != '':
                                item[copy_key] = fillter_item.get(copy_key)
            return item, diff_flag

        if isinstance(item, ProjectBaseItem):
            query = {'project_no': item['project_no']}
            table_name = ProjectBaseItem.table_name
            load_item = DefaultItemLoader(item=ProjectBaseItem())

        elif isinstance(item, BuildingItem):
            query = {'building_no': item['building_no']}
            table_name = BuildingItem.table_name
            load_item = DefaultItemLoader(item=BuildingItem())

        elif isinstance(item, OpeningunitItem):
            query = {'opening_unit_no': item['opening_unit_no']}
            table_name = OpeningunitItem.table_name
            load_item = DefaultItemLoader(item=OpeningunitItem())

        elif isinstance(item, HouseItem):
            query = {'house_no': item['house_no']}
            table_name = HouseItem.table_name
            load_item = DefaultItemLoader(item=HouseItem())

        else:
            raise DropItem("not in Item")

        for key in item.fields.keys():
            load_item.add_value(key, item.get(key, ''))
        item = load_item.load_item()

        res_item = self.find_latest_one(table_name, query)
        if res_item:
            update = {'$set': {'NewCurTimeStamp': datetime.datetime.now()}}
            self.find_latest_one_update(table_name, query, update)
            item, diff_flag = check_item_change(res_item, item)
        else:
            diff_flag = True

        return item, diff_flag

    def storage_item(self, item):
        table_name = self.table_name
        self.mongodb[table_name].insert(item)
        logger.debug("storage item: %(item)s",
                     {'item': item})

    def process_item(self, item, spider):
        self.table_name = item.table_name
        if item:
            item['CurTimeStamp'] = str(datetime.datetime.now())
            item['NewCurTimeStamp'] = str(datetime.datetime.now())
            diff_item, diff_flag = self.check_item(item)
            if diff_flag:
                self.storage_item(diff_item)
            return diff_item
