# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import datetime
from sqlalchemy.orm import sessionmaker
from models.job_models import JobData
from sqlalchemy import create_engine

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))
logger = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self, settings):
        self.settings = settings
        engine = create_engine('mysql+pymysql://root:password@xxxx/job_data?charset=utf8')
        JobData.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

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
        check_item_flag = False
        session = self.Session()
        q_object = session.query(JobData)
        res_object = q_object.filter(JobData.JobUUID == item['JobUUID']).order_by(JobData.RecordTime).first()
        if res_object:
            for key in item:
                if self.safe_format_value(item.get(key)) != self.safe_format_value(getattr(res_object, key)):
                    check_item_flag = True
        return check_item_flag


    def process_item(self, item, spider):
        session = self.Session()
        check_item_flag = self.check_item(item)
        print(check_item_flag)
        if not self.check_item(item):
            JobItem = JobData(**item)
            session.add(JobItem)  # 添加数据
            session.commit()  # 保存修改
        return item
