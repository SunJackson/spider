# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseAdmin.HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBase

class OpeningunitItem(DjangoItem):
    django_model = OpeningunitBase

class BuildingItem(DjangoItem):
    django_model = BuildingBase

class HouseItem(DjangoItem):
    django_model = HouseBase


class SearchHouseItem(DjangoItem):
    django_model = SearchHouse
