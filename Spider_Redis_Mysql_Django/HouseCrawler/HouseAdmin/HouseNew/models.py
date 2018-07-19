# !/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class ResidentialArea(models.Model):
    TID = models.BigAutoField(primary_key=True)
    TGuid = models.CharField(default='', max_length=40, blank=True, null=True)
    CreatedDate = models.DateTimeField(blank=True, null=True)
    State = models.IntegerField(blank=True, null=True)
    ModifyDate = models.DateTimeField(blank=True, null=True)
    GroundCarsAmount = models.IntegerField(blank=True, null=True)
    UndergroundCarsAmount = models.IntegerField(blank=True, null=True)
    GroundMonthlyRent = models.FloatField(blank=True, null=True)
    UndergroundMonthlyRent = models.FloatField(blank=True, null=True)
    ManagementFees = models.FloatField(blank=True, null=True)
    ManagementFeesDesp = models.CharField(max_length=255, blank=True, null=True)
    ManagementCompany = models.CharField(max_length=255, blank=True, null=True)
    ManagementCompanyLevel = models.CharField(max_length=100, blank=True, null=True)
    ManagementScore = models.CharField(max_length=100, blank=True, null=True)
    SafetyCompany = models.CharField(max_length=255, blank=True, null=True)
    RingRoad = models.CharField(max_length=255, blank=True, null=True)
    GreeningRate = models.FloatField( blank=True, null=True)
    PositionInfo = models.TextField(default='', blank=True, null=True)
    ParkingSpaceInfo = models.TextField(default='', blank=True, null=True)
    BaseFacility = models.TextField(default='', blank=True, null=True)
    EnvironmentInfo = models.TextField(default='', blank=True, null=True)
    PublicSecurity = models.TextField(default='', blank=True, null=True)
    StreetSituation = models.TextField(default='', blank=True, null=True)
    PeripheralSupporting = models.TextField(blank=True, null=True)
    TrafficInfo = models.TextField(default='', blank=True, null=True)
    Tags = models.CharField(default='', max_length=255, blank=True, null=True)
    PlanningInfo = models.TextField(default='', blank=True, null=True)
    Description = models.TextField(default='', blank=True, null=True)
    DistanceFromPlaces = models.TextField(blank=True, null=True)
    Location = models.CharField(default='',
                                max_length=255, blank=True, null=True)
    Roads = models.TextField(default='', blank=True, null=True)
    TrafficLimited = models.TextField(blank=True, null=True)
    ParkingEasy = models.CharField(default='', max_length=100, blank=True, null=True)
    OtherFacility = models.TextField(default='', blank=True, null=True)
    OutsideDevelopedLevel = models.CharField(default='',
                                             max_length=255, blank=True, null=True)
    RoomRate = models.FloatField(blank=True, null=True)
    DecorationInfo = models.CharField(default='', max_length=1000, blank=True, null=True)
    PriceDifferenceType = models.CharField(
        default='', max_length=100, blank=True, null=True)
    PriceDifferenceInfo = models.TextField(default='', blank=True, null=True)
    HouseTypes = models.CharField(default='', max_length=150, blank=True, null=True)
    HouseStructureDesp = models.TextField(default='', blank=True, null=True)
    MainApartment = models.CharField(default='', max_length=255, blank=True, null=True)
    IsMoreSmallUnits = models.SmallIntegerField(blank=True, null=True)
    DistrictName = models.CharField(default='', max_length=255, blank=True, null=True)
    ResidentialAreaName = models.CharField(default='', max_length=255, blank=True, null=True)
    ResidentialAreaType = models.CharField(default='', max_length=100, blank=True, null=True)
    Address = models.CharField(default='', max_length=255, blank=True, null=True)
    DeveloperCompany = models.CharField(default='', max_length=255, blank=True, null=True)
    SellDate = models.DateTimeField(blank=True, null=True)
    CompletionDate = models.DateTimeField(blank=True, null=True)
    HouseBuildingCount = models.IntegerField(blank=True, null=True)
    MaxFloors = models.IntegerField(blank=True, null=True)
    HousingCount = models.IntegerField(blank=True, null=True)
    FloorAreaRatio = models.FloatField(blank=True, null=True)
    BuildingArea = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    BuildingCategorys = models.CharField(
        default='', max_length=255, blank=True, null=True)
    BuildingInfo = models.TextField(default='', blank=True, null=True)
    LandShape = models.CharField(default='', max_length=100, blank=True, null=True)
    Dixing = models.CharField(default='', max_length=100, blank=True, null=True)
    Terrain = models.CharField(default='', max_length=100, blank=True, null=True)
    LandDevelopedLevel = models.CharField(default='',
                                          max_length=255, blank=True, null=True)
    LandArea = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    SaleStatus = models.CharField(default='', max_length=10, blank=True, null=True)
    BorderDistrictName = models.CharField(
        default='',
        max_length=255, blank=True, null=True)
    LandMaxUseYearsLimit = models.IntegerField(blank=True, null=True)
    LandUseYearsLimitDescribe = models.CharField(
        default='', max_length=1000, blank=True, null=True)
    RegionName = models.CharField(default='', max_length=50, blank=True, null=True)
    BorderRegionName = models.CharField(default='', max_length=50, blank=True, null=True)
    Remarks = models.TextField(default='', blank=True, null=True)
    URLID = models.CharField(default='',
                             max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=[
                'TGuid',

            ]),
        ]

    def __repr__(self):
        return "{}".format(self.__class__.__name__)


class RAPicture(models.Model):
    TID = models.BigAutoField(primary_key=True)
    TGuid = models.CharField(default='', max_length=40, blank=True, null=True)
    CreatedDate = models.DateTimeField(blank=True, null=True)
    State = models.IntegerField(blank=True, null=True)
    ModifyDate = models.DateTimeField(blank=True, null=True)
    ResidentialAreaID = models.BigIntegerField(blank=True, null=True)
    PictureResourceID = models.BigIntegerField(blank=True, null=True)
    PictureName = models.CharField(default='', max_length=255, blank=True, null=True)
    RAImageCategories = models.CharField(default='', max_length=50, blank=True, null=True)
    URLID = models.CharField(default='',
                             max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=[
                'TGuid',

            ]),
        ]


class RANameInfo(models.Model):
    TID = models.BigAutoField(primary_key=True)
    TGuid = models.CharField(default='', max_length=40, blank=True, null=True)
    CreatedDate = models.DateTimeField(blank=True, null=True)
    State = models.IntegerField(blank=True, null=True)
    ModifyDate = models.DateTimeField(blank=True, null=True)
    ResidentialAreaID = models.BigIntegerField(blank=True, null=True)
    NameInSource = models.CharField(default='', max_length=255, blank=True, null=True)
    Source = models.CharField(default='', max_length=255, blank=True, null=True)
    SourceKey = models.CharField(default='', max_length=255, blank=True, null=True)
    SourceUrl = models.TextField(default='', blank=True, null=True)
    NameType = models.CharField(default='', max_length=50, blank=True, null=True)
    FirstLetter = models.CharField(default='', max_length=255, blank=True, null=True)
    LanguageType = models.CharField(default='', max_length=10, blank=True, null=True)
    PinYin = models.CharField(default='', max_length=500, blank=True, null=True)
    NameTags = models.CharField(default='', max_length=255, blank=True, null=True)
    DistrictName = models.CharField(default='', max_length=255, blank=True, null=True)
    Remarks = models.TextField(default='', blank=True, null=True)
    URLID = models.CharField(default='',
                             max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=[
                'TGuid',

            ]),
        ]


class RACoordinate(models.Model):
    TID = models.BigAutoField(primary_key=True)
    TGuid = models.CharField(default='', max_length=40, blank=True, null=True)
    CreatedDate = models.DateTimeField(blank=True, null=True)
    State = models.IntegerField(blank=True, null=True)
    ModifyDate = models.DateTimeField(blank=True, null=True)
    ResidentialAreaID = models.BigIntegerField(blank=True, null=True)
    MapType = models.CharField(default='', max_length=100, blank=True, null=True)
    XLongitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    YLatitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    XYCoordinateArray = models.TextField(default='', blank=True, null=True)
    URLID = models.CharField(default='',
                             max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=[
                'TGuid',

            ]),
        ]
