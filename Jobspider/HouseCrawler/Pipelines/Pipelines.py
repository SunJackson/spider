# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import datetime
from sqlalchemy.orm import sessionmaker
from HouseCrawler.models.job_models import JobData
from HouseCrawler.Items.Items import JobBaseItem
from sqlalchemy import create_engine

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))
logger = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self, settings):
        self.settings = settings
        engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/job_data?charset=utf8mb4')
        JobData.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        self.num = 0

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
        check_item_flag = True
        close_table = ['ReleaseTime', 'RecordTime', 'Ka', 'DataJid', 'DataLid']
        q_object = self.session.query(JobData)
        res_object = q_object.filter(JobData.JobUUID == item['JobUUID']).order_by(JobData.RecordTime).first()
        if res_object:
            check_item_flag = False
            for key in item:
                if key in close_table:
                    continue
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    check_item_flag = True
        return check_item_flag

    def process_item(self, item, spider):
        if isinstance(item,JobBaseItem):
            check_item_flag = self.check_item(item)
            item['RecordTime'] = datetime.datetime.now()
            if check_item_flag:
                self.process_chunck_item(item, spider)
        return item

    def process_chunck_item(self, item, spider):
        self.num += 1
        JobItem = JobData(**item)
        self.session.add(JobItem)  # 添加数据
        if self.num > 100:
            print('storeItem')
            self.session.commit()
            self.num = 0


