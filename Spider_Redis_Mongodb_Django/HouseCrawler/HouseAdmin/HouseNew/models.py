# -*- coding: utf-8 -*-
#!/usr/bin/python
import uuid
import datetime
from django_mongoengine import *

from django_mongoengine import fields


class ProjectBaseShanghai(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    project_id = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                  binary=False, null=False)
    project_sts = fields.StringField(default='', max_length=255, null=False)

    project_addr = fields.StringField(default='', max_length=255, null=False)
    project_house_num = fields.StringField(default='', max_length=255, null=False)
    project_house_area = fields.StringField(default='', max_length=255, null=False)
    project_no = fields.StringField(default='', max_length=255, null=False)
    project_name = fields.StringField(default='', max_length=255, null=False)
    project_county = fields.StringField(default='', max_length=255, null=False)
    project_blank = fields.StringField(default='', max_length=255, null=False)
    project_com_name = fields.StringField(default='', max_length=255, null=False)

    project_price = fields.StringField(default='', max_length=255, null=False)
    project_price_house = fields.StringField(default='', max_length=255, null=False)
    project_price_back = fields.StringField(default='', max_length=255, null=False)
    project_price_house_back = fields.StringField(default='', max_length=255, null=False)
    project_detail_link = fields.StringField(default='', max_length=510, null=False)
    change_data = fields.StringField(default='', max_length=1024, null=False)

    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'NewCurTimeStamp',
            'project_detail_link',
            'change_data',
            'project_id',
            'project_no',

        ]
    }


class OpeningunitBaseShanghai(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    project_no = fields.StringField(default='', max_length=255, null=False)
    project_name = fields.StringField(default='', max_length=255, null=False)
    opening_unit_no = fields.StringField(default='', max_length=255, null=False)
    opening_building_detail_link = fields.StringField(default='', max_length=510, null=False)
    opening_unit_licence = fields.StringField(default='', max_length=255, null=False)
    opening_unit_opendate = fields.StringField(default='', max_length=255, null=False)
    opening_unit_num = fields.StringField(default='', max_length=255, null=False)
    opening_unit_housenum = fields.StringField(default='', max_length=255, null=False)
    opening_unit_area = fields.StringField(default='', max_length=255, null=False)
    opening_unit_housearea = fields.StringField(default='', max_length=255, null=False)
    opening_unit_sts = fields.StringField(default='', max_length=255, null=False)
    change_data = fields.StringField(default='', max_length=1024, null=False)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'NewCurTimeStamp',
            'opening_unit_sts',
            'change_data',
            'project_no',
            'opening_unit_no',
        ]
    }


class BuildingBaseShanghai(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    project_no = fields.StringField(default='', max_length=255, null=False)
    project_name = fields.StringField(default='', max_length=255, null=False)
    opening_unit_no = fields.StringField(default='', max_length=255, null=False)
    building_name = fields.StringField(default='', max_length=255, null=False)
    building_no = fields.StringField(default='', max_length=255, null=False)
    building_price = fields.StringField(default='', max_length=255, null=False)
    building_fluctuation = fields.StringField(default='', max_length=255, null=False)
    building_num = fields.StringField(default='', max_length=255, null=False)
    building_area = fields.StringField(default='', max_length=255, null=False)
    building_sts = fields.StringField(default='', max_length=255, null=False)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    building_url = fields.URLField(default=None, null=True, blank=True)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'NewCurTimeStamp',
            'change_data',
            'project_no',
            'building_sts',
            'opening_unit_no',
            'building_no',

        ]
    }


class HouseBaseShanghai(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    project_name = fields.StringField(default='', max_length=255, null=False)
    project_no = fields.StringField(default='', max_length=255, null=False)
    opening_unit_no = fields.StringField(default='', max_length=255, null=False)
    building_no = fields.StringField(default='', max_length=255, null=False)
    house_no = fields.StringField(default='', max_length=255, null=False)
    house_floor = fields.StringField(default='', max_length=255, null=False)
    house_num = fields.StringField(default='', max_length=255, null=False)
    house_class = fields.StringField(default='', max_length=255, null=False)
    house_use_type = fields.StringField(default='', max_length=255, null=False)
    house_layout = fields.StringField(default='', max_length=255, null=False)
    house_area_pr_yc = fields.StringField(default='', max_length=510, null=False)
    house_area_pr_tn = fields.StringField(default='', max_length=255, null=False)
    house_area_pr_ft = fields.StringField(default='', max_length=255, null=False)
    house_area_pr_dx = fields.StringField(default='', max_length=255, null=False)
    house_area_real_yc = fields.StringField(default='', max_length=255, null=False)
    house_area_real_tn = fields.StringField(default='', max_length=255, null=False)
    house_area_real_ft = fields.StringField(default='', max_length=255, null=False)
    house_area_real_dx = fields.StringField(default='', max_length=255, null=False)
    house_sts = fields.StringField(default='', max_length=255, null=False)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    house_stsLatest = fields.StringField(default='', max_length=255, null=False)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'NewCurTimeStamp',
            'house_stsLatest',
            'house_sts',
            'change_data',
            'project_no',
            'opening_unit_no',
            'building_no',
            'house_no',
        ]
    }
