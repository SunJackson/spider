# -*- coding: utf-8 -*-
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ResidentialAreaItem(DjangoItem):
    django_model = ResidentialArea


class RAPictureItem(DjangoItem):
    django_model = RAPicture


class RANameInfoItem(DjangoItem):
    django_model = RANameInfo


class RACoordinateItem(DjangoItem):
    django_model = RACoordinate