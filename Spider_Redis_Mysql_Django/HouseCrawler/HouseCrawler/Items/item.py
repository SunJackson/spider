# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Field
import logging
import time
from scrapy.loader.processors import MapCompose, TakeFirst

def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        result = time.strptime(str, "%Y-%m-%d")
        return result
    except:
        return None


def is_valid_int(str):
    '''判断是否是一个int类型'''
    try:
        result = int(str)
        return result
    except:
        return None


def is_valid_float(str):
    '''判断是否是一个float类型'''
    try:
        result = float(str)
        return result
    except:
        return None


class ResidentialAreaItem(scrapy.Item):
    _id = Field()
    TID = Field()
    TGuid = Field()
    CreatedDate = Field(input_processor=MapCompose(is_valid_date))
    State = Field(input_processor=MapCompose(is_valid_int))
    ModifyDate = Field(input_processor=MapCompose(is_valid_date))
    GroundCarsAmount = Field(input_processor=MapCompose(is_valid_int))
    UndergroundCarsAmount = Field(input_processor=MapCompose(is_valid_int))
    GroundMonthlyRent = Field(input_processor=MapCompose(is_valid_float))
    UndergroundMonthlyRent = Field(input_processor=MapCompose(is_valid_float))
    ManagementFees = Field(input_processor=MapCompose(is_valid_float))
    ManagementFeesDesp = Field()
    ManagementCompany = Field()
    ManagementCompanyLevel = Field()
    ManagementScore = Field()
    SafetyCompany = Field()
    RingRoad = Field()
    GreeningRate = Field(input_processor=MapCompose(is_valid_float))
    PositionInfo = Field()
    ParkingSpaceInfo = Field()
    BaseFacility = Field()
    EnvironmentInfo = Field()
    PublicSecurity = Field()
    StreetSituation = Field()
    PeripheralSupporting = Field()
    TrafficInfo = Field()
    Tags = Field()
    PlanningInfo = Field()
    Description = Field()
    DistanceFromPlaces = Field()
    Location = Field()
    Roads = Field()
    TrafficLimited = Field()
    ParkingEasy = Field()
    OtherFacility = Field()
    OutsideDevelopedLevel = Field()
    RoomRate = Field(input_processor=MapCompose(is_valid_float))
    DecorationInfo = Field()
    PriceDifferenceType = Field()
    PriceDifferenceInfo = Field()
    HouseTypes = Field()
    HouseStructureDesp = Field()
    MainApartment = Field()
    IsMoreSmallUnits = Field()
    DistrictName = Field()
    ResidentialAreaName = Field()
    ResidentialAreaType = Field()
    Address = Field()
    DeveloperCompany = Field()
    SellDate = Field(input_processor=MapCompose(is_valid_date))
    CompletionDate = Field(input_processor=MapCompose(is_valid_date))
    HouseBuildingCount = Field(input_processor=MapCompose(is_valid_int))
    MaxFloors = Field(input_processor=MapCompose(is_valid_int))
    HousingCount = Field(input_processor=MapCompose(is_valid_int))
    FloorAreaRatio = Field(input_processor=MapCompose(is_valid_float))
    BuildingArea = Field(input_processor=MapCompose(is_valid_float))
    BuildingCategorys = Field()
    BuildingInfo = Field()
    LandShape = Field()
    Dixing = Field()
    Terrain = Field()
    LandDevelopedLevel = Field()
    LandArea = Field(input_processor=MapCompose(is_valid_float))
    SaleStatus = Field()
    BorderDistrictName = Field()
    LandMaxUseYearsLimit = Field()
    LandUseYearsLimitDescribe = Field(input_processor=MapCompose(is_valid_int))
    RegionName = Field()
    BorderRegionName = Field()
    Remarks = Field()
    URLID = Field()


class RAPictureItem(scrapy.Item):
    _id = Field()
    TID = Field()
    TGuid = Field()
    CreatedDate = Field()
    State = Field(input_processor=MapCompose(is_valid_int))
    ModifyDate = Field()
    ResidentialAreaID = Field()
    PictureResourceID = Field()
    PictureName = Field()
    RAImageCategories = Field()
    URLID = Field()


class RANameInfoItem(scrapy.Item):
    _id = Field()
    TID = Field()
    TGuid = Field()
    CreatedDate = Field(input_processor=MapCompose(is_valid_date))
    State = Field(input_processor=MapCompose(is_valid_int))
    ModifyDate = Field(input_processor=MapCompose(is_valid_date))
    ResidentialAreaID = Field()
    NameInSource = Field()
    Source = Field()
    SourceKey = Field()
    SourceUrl = Field()
    NameType = Field()
    FirstLetter = Field()
    LanguageType = Field()
    PinYin = Field()
    NameTags = Field()
    DistrictName = Field()
    Remarks = Field()
    URLID = Field()


class RACoordinateItem(scrapy.Item):
    _id = Field()
    TID = Field()
    TGuid = Field()
    CreatedDate = Field(input_processor=MapCompose(is_valid_date))
    State = Field(input_processor=MapCompose(is_valid_int))
    ModifyDate = Field(input_processor=MapCompose(is_valid_date))
    ResidentialAreaID = Field()
    MapType = Field()
    XLongitude = Field(input_processor=MapCompose(is_valid_float))
    YLatitude = Field(input_processor=MapCompose(is_valid_float))
    XYCoordinateArray = Field()
    URLID = Field()
