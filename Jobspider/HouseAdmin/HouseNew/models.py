# -*- coding: utf-8 -*-
#!/usr/bin/python
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields
class MonitorProjectBaseWuxi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=10240, null=False)
    ProjectNo =  fields.StringField(default='', max_length=255, null=False)
    ProjectName =  fields.StringField(default='', max_length=255, null=False)
    TotalHouseNumber = fields.StringField(default='', max_length=255,)
    OnSoldNumber = fields.StringField(default='', max_length=255,)
    PresalePermitNumber = fields.StringField(default='', max_length=255,)
    ProjectCode = fields.StringField(default='', max_length=255,)
    projectDetailUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'change_data',
            'ProjectNo',
            'ProjectCode'
        ]
    }
class ProjectBaseWuxi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=10240, null=False)
    ProjectNo =  fields.StringField(default='', max_length=255, null=False)
    TotalHouseNumber = fields.StringField(default='', max_length=255,)
    OnSoldNumber = fields.StringField(default='', max_length=255,)
    SoldNumber = fields.StringField(default='', max_length=255,)
    LimitSoldNumber = fields.StringField(default='', max_length=255,)
    ProjectName = fields.StringField(default='', max_length=255,)
    PresalePermitNumber = fields.StringField(default='', max_length=255,)
    ProjectTemporaryName = fields.StringField(default='', max_length=255,)
    ApprovalPresaleDepartment = fields.StringField(default='', max_length=255,)
    Developer = fields.StringField(default='', max_length=255,)
    DeveloperUrl = fields.StringField(default='', max_length=255,)
    Cooperator = fields.StringField(default='', max_length=255,)
    ProjectAddress = fields.StringField(default='', max_length=255,)
    DistrictName = fields.StringField(default='', max_length=255,)
    ApprovalForApproval = fields.StringField(default='', max_length=255,)
    UsePermitNumber = fields.StringField(default='', max_length=255,)
    OwnedLand = fields.StringField(default='', max_length=255,)
    ConstructionPermitNumber = fields.StringField(default='', max_length=255,)
    CertificateOfUseOfStateOwnedLand = fields.StringField(default='', max_length=255,)
    PreSaleAreas = fields.StringField(default='', max_length=255,)
    SaleCom = fields.StringField(default='', max_length=255,)
    SaleComPhone = fields.StringField(default='', max_length=255,)
    SaleAddress = fields.StringField(default='', max_length=255,)
    SalePhone = fields.StringField(default='', max_length=255,)
    ManagementCompany = fields.StringField(default='', max_length=255,)
    SoldStatusInfo = fields.DictField(default={'0': '0'})
    GetSoldStatusUrl = fields.URLField(default=None,  blank=True)
    BuildingBaseUrl = fields.URLField(default=None,  blank=True)
    SourceUrl = fields.URLField(default=None,  blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectNo',
            'OnSoldNumber',
            'SoldNumber'
            ]
           }
class MonitorHouseBaseWuxi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=10240, null=False)
    ProjectName =  fields.StringField(default='', max_length=255, null=False)
    BuildingNum = fields.StringField(default='', max_length=255, null=False)
    HouseTitle = fields.StringField(default='', max_length=255, null=False)
    HouseNo = fields.StringField(default='', max_length=255, null=False)
    HouseFwid = fields.StringField(default='', max_length=255, null=False)
    HouseLpid = fields.StringField(default='', max_length=255, null=False)
    HouseSts = fields.StringField(default='', max_length=255, null=False)
    HouseStsLatest = fields.StringField(default='', max_length=255, null=False)
    HouseInfoUrl = fields.URLField(default=None, blank=True)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'change_data',
            'HouseNo',
            'HouseSts',
            ]
           }
class DeveloperBaseWuxi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=10240, null=False)
    DeveloperNo =  fields.StringField(default='', max_length=255, null=False)
    DeveloperName = fields.StringField(default='', max_length=255,)
    DeveloperAddress = fields.StringField(default='', max_length=255,)
    DeveloperFullName = fields.StringField(default='', max_length=255,)
    DeveloperLevel = fields.StringField(default='', max_length=255,)
    LegalPerson = fields.StringField(default='', max_length=255,)
    SalesManager = fields.StringField(default='', max_length=255,)
    ZipCode = fields.StringField(default='', max_length=255,)
    Fax = fields.StringField(default='', max_length=255,)
    Web = fields.StringField(default='', max_length=255,)
    EMail = fields.StringField(default='', max_length=255,)
    ProjectName = fields.StringField(default='', max_length=255,)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'DeveloperNo',
            'DeveloperAddress',
            ]
           }
class HouseBaseWuxi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=10240, null=False)
    HouseNo =  fields.StringField(default='', max_length=255, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    BuildingNum = fields.StringField(default='', max_length=255, null=False)
    HouseAddress = fields.StringField(default='', max_length=255, null=False)
    HouseCode = fields.StringField(default='', max_length=255, null=False)
    HouseSts = fields.StringField(default='', max_length=255, null=False)
    HouseStsLatest = fields.StringField(default='', max_length=255, null=False)
    BuildingNumber = fields.StringField(default='', max_length=255, null=False)
    UnitNumber = fields.StringField(default='', max_length=255, null=False)
    HouseNumber = fields.StringField(default='', max_length=255, null=False)
    ActualFloor = fields.StringField(default='', max_length=255, null=False)
    TotalFloor = fields.StringField(default='', max_length=255, null=False)
    BuildingStructure = fields.StringField(default='', max_length=255, null=False)
    HouseUseType = fields.StringField(default='', max_length=255, null=False)
    AreasType = fields.StringField(default='', max_length=255, null=False)
    TotalArea = fields.StringField(default='', max_length=255, null=False)
    InsideOfBuildingArea = fields.StringField(default='', max_length=255, null=False)
    MeasuredSharedPublicArea = fields.StringField(default='', max_length=255, null=False)
    hightArea = fields.StringField(default='', max_length=255, null=False)
    Remarks = fields.StringField(default='', max_length=255, null=False)
    Price = fields.StringField(default='', max_length=255, null=False)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'HouseNo',
            'HouseSts',
            'HouseStsLatest'
            ]
           }
