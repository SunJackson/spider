# -*- coding: utf-8 -*-
#!/usr/bin/python
import scrapy


class JobBaseItem(scrapy.Item):
    RecordTime = scrapy.Field()
    JobUUID = scrapy.Field()
    CityName = scrapy.Field()
    CityCode = scrapy.Field()
    JobTitle = scrapy.Field()
    Pay = scrapy.Field()
    Region = scrapy.Field()
    WorkYears = scrapy.Field()
    Education = scrapy.Field()
    Industry = scrapy.Field()
    Financing = scrapy.Field()
    People = scrapy.Field()
    Company = scrapy.Field()
    CompanyUrl = scrapy.Field()
    Publisher = scrapy.Field()
    PublisherPosition = scrapy.Field()
    ReleaseTime = scrapy.Field()
    Ka = scrapy.Field()
    DataJid = scrapy.Field()
    DataLid = scrapy.Field()
    JobDetail = scrapy.Field()
    CompanyDetail = scrapy.Field()
    CompanyName = scrapy.Field()
    LegalRepresentative = scrapy.Field()
    RegisteredCapital = scrapy.Field()
    ResTime = scrapy.Field()
    CompanyType = scrapy.Field()
    ManageState = scrapy.Field()
    LoactionAddress = scrapy.Field()

