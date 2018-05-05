# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
from sqlalchemy.orm import sessionmaker
from models.job_models import JobData
from sqlalchemy import create_engine

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))
logger = logging.getLogger(__name__)


class Pipeline(object):
    def __init__(self):
        engine = create_engine('mysql+pymysql://root:password@120.78.189.152:3306/job_data?charset=utf8')
        JobData.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        # try:
        session = self.Session()
        JobItem = JobData(**item)
        session.add(JobItem)  # 添加数据
        session.commit()  # 保存修改
        # except Exception as e:
        #     print(e)
        return item
