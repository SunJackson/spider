from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
import datetime
import uuid


def filter_time(value):
    if value is not None and value != '':
        return datetime.datetime.now()


def filter_id(value):
    if value is not None and value != '':
        return uuid.uuid1()


def filter_data(value):
    if value is not None and value != '':
        return value


class ProjectBaseItem(Item):
    table_name = 'project_base_shanghai'
    _id = Field(input_processor=MapCompose(filter_id))
    RecordID = Field(input_processor=MapCompose(filter_id))
    CurTimeStamp = Field(input_processor=MapCompose(filter_time))
    project_id = Field()
    project_sts = Field()
    project_addr = Field()
    project_house_num = Field()
    project_house_area = Field()
    project_no = Field()
    project_name = Field()
    project_county = Field()
    project_blank = Field()
    project_com_name = Field()
    project_price = Field()
    project_price_house = Field()
    project_price_back = Field()
    project_price_house_back = Field()
    project_detail_link = Field()
    change_data = Field()
    NewCurTimeStamp = Field()

class OpeningunitItem(Item):
    table_name = 'openingunit_base_shanghai'
    _id = Field(input_processor=MapCompose(filter_id) )
    RecordID = Field(input_processor=MapCompose(filter_id))
    CurTimeStamp = Field(input_processor=MapCompose(filter_time))
    project_no = Field()
    project_name = Field()
    opening_unit_no = Field()
    opening_building_detail_link = Field()
    opening_unit_licence = Field()
    opening_unit_opendate = Field()
    opening_unit_num = Field()
    opening_unit_housenum = Field()
    opening_unit_area = Field()
    opening_unit_housearea = Field()
    opening_unit_sts = Field()
    change_data = Field()
    NewCurTimeStamp = Field()

class BuildingItem(Item):
    table_name = 'building_base_shanghai'
    _id = Field(input_processor=MapCompose(filter_id) )
    RecordID = Field(input_processor=MapCompose(filter_id))
    CurTimeStamp = Field(input_processor=MapCompose(filter_time))
    project_no = Field()
    project_name = Field()
    opening_unit_no = Field()
    building_name = Field()
    building_no = Field()
    building_price = Field()
    building_fluctuation = Field()
    building_num = Field()
    building_area = Field()
    building_sts = Field()
    change_data = Field()
    building_url = Field()
    NewCurTimeStamp = Field()


class HouseItem(Item):
    table_name = 'house_base_shanghai'
    _id = Field(input_processor=MapCompose(filter_id))
    RecordID = Field(input_processor=MapCompose(filter_id))
    CurTimeStamp = Field(input_processor=MapCompose(filter_time))
    project_name = Field()
    project_no = Field()
    opening_unit_no = Field()
    building_no = Field()
    house_no = Field()
    house_floor = Field()
    house_num = Field()
    house_class = Field()
    house_use_type = Field()
    house_layout = Field()
    house_area_pr_yc = Field()
    house_area_pr_tn = Field()
    house_area_pr_ft = Field()
    house_area_pr_dx = Field()
    house_area_real_yc = Field()
    house_area_real_tn = Field()
    house_area_real_ft = Field()
    house_area_real_dx = Field()
    house_sts = Field()
    change_data = Field()
    house_stsLatest = Field()
    NewCurTimeStamp = Field()
