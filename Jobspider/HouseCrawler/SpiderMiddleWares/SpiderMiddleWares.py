#!/usr/python3
# -*- coding: utf-8 -*-
import sys
import uuid
import re
import copy
import json
import logging
import random
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.Items import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
'''
    Created on 2017-11-29 12:44:32.
'''
class SpiderMiddlerGetJsonDate(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-devtools-emulate-network-conditions-client-id': "5CB00670C9C98DBAA2CFEE9F04E34EA3",
        'x-requested-with': "XMLHttpRequest",
        'referer': "https://www.zhipin.com/",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cookie': "lastCity=101280100; JSESSIONID=\"\"; __g=-; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D%26scity%3D101280100%26industry%3D%26position%3D; __c=1525243636; __l=r=https%3A%2F%2Fwww.zhipin.com%2F&l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D%26scity%3D101280100%26industry%3D%26position%3D; __a=29424214.1525243551.1525243551.1525243636.8.2.7.8",
        'cache-control': "no-cache",
         }
       


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'GetCitys':
            logging.debug("GetCitys")

            citys_url = 'https://www.zhipin.com/common/data/city.json'
            cityurl = 'https://www.zhipin.com/job_detail/?query=&scity=101020100&industry=&position='
            headers = self.headers
            result.append(Request(url = cityurl,
                                                      headers = headers,
                                                      method = 'GET',
                                                      meta = {
                                                          'PageType': 'CityJobs',
                                                      }))

        if response.meta.get('PageType') == 'CityJobs':
            logging.debug("CityJobs")
            list_page = Selector(response).xpath('//*[@id="main"]/div/div[2]/div[2]/a')
            havenext = list_page[-1].xpath('./@class').extract_first()
            jobdatas = Selector(response).xpath('//*[@id="main"]/div/div[2]/ul/li')
            for jobdata in jobdatas:
                #job_title://*[@id="main"]/div/div[2]/ul/li[2]/div/div[1]/h3/a/div[1]
                job_title = jobdata.xpath('./div/div[1]/h3/a/div[1]/text()').extract_first()
                print(job_title)
            print(havenext)
            if havenext == 'next':
                urlnext =  'https://www.zhipin.com' + list_page[-1].xpath('./@href').extract_first()
                result.append(Request(url = urlnext,
                                                      method = 'GET',
                                                      meta = {
                                                          'PageType': 'CityJobs',
                                                      }))
        return result


    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerBuildingBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'no-cache',
            'Connection': 'keep - alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.wxhouse.com:9097',
        }



    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def get_house_sts(sts):
            houseSts = ''
            houseStsClass = {
                'background-color:#33FF00;': '待售',
                'background-color:#FFFF00;': '已售',
                'background-color:#CC9933;': '保留',
                'background-color:#CCCCCC;': '抵押',
                'background-color:#FF9900;': '已预定',
                'background-color:#0000FF;': '自持',
                'background-color:#993300;': '查封',
            }
            if sts in houseStsClass.keys():
                houseSts = houseStsClass[sts]
            return houseSts


        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'BuildingBase':
            logging.debug("BuildingBase")
            ProjectName = response.meta.get('ProjectName')
            buildingTables = Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[1]/td/b')
            for buildingTable in buildingTables:
                buildingUrl = re.search(r"viewGlt\('(.*?)','(.*?)'\)",
                                        buildingTable.xpath('./a/@onclick').extract_first())
                BuildingNum = check_data_str(buildingTable.xpath('./a/text()').extract_first())
                BuildingNo = uuid.uuid3(uuid.NAMESPACE_DNS,
                                        ProjectName + str(buildingUrl.group(1)) + str(buildingUrl.group(2))).hex
                headers = self.headers
                headers['Referer'] = response.url
                randit = random.random()
                houseDetailsUrl = 'http://www.wxhouse.com:9097/wwzs/viewFwGlt.action?lpid=%s&zh=%s&it=%s' \
                               % (str(buildingUrl.group(1)), str(buildingUrl.group(2)), str(randit))
                logging.debug('houseDetails' + houseDetailsUrl)
                if houseDetailsUrl:
                    # project_base = {
                    #     'source_url': houseDetailsUrl,
                    #     'headers': headers,
                    #     'method': 'GET',
                    #     'meta': {
                    #         'PageType': 'BuildingInfo',
                    #         'ProjectName': ProjectName,
                    #         'BuildingNum': BuildingNum,
                    #         'BuildingNo': BuildingNo
                    #     }}
                    #
                    # project_base_json = json.dumps(project_base, sort_keys=True)
                    # self.r.sadd('WuxiCrawler:start_urls', project_base_json)

                    result.append(Request(url = houseDetailsUrl,
                                          headers = headers,
                                          method = 'GET',
                                          meta = {
                                              'PageType': 'BuildingInfo',
                                              'ProjectName': ProjectName,
                                              'BuildingNum': BuildingNum,
                                              'BuildingNo': BuildingNo
                                          }))

        if response.meta.get('PageType') == 'BuildingInfo':
            logging.debug('BuildingInfo')
            ProjectName = response.meta.get('ProjectName')
            BuildingNum = response.meta.get('BuildingNum')
            num = 0
            GetHouses = Selector(response).xpath('/html/body/div[1]/div')
            for GetHouse in GetHouses:
                HouseClass = check_data_str(GetHouse.xpath('./@class').extract_first())
                if HouseClass == 'LPBFW_BOROR':
                    monitorhousebaseitem = MonitorHouseBaseItem()
                    monitorhousebaseitem['ProjectName'] = ProjectName
                    monitorhousebaseitem['BuildingNum'] = BuildingNum
                    HouseTitle = check_data_str(GetHouse.xpath('./@title').extract_first())
                    monitorhousebaseitem['HouseTitle'] = HouseTitle

                    HouseNo = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectName + BuildingNum + str(HouseTitle) + str(num)).hex
                    monitorhousebaseitem['HouseNo'] = HouseNo
                    num = num + 1
                    GetHouseSts = check_data_str(GetHouse.xpath('./div/@style').extract_first())
                    if GetHouseSts:
                        HouseSts = get_house_sts(GetHouseSts)
                        monitorhousebaseitem['HouseSts'] = HouseSts
                        HouseFwid = check_data_str(GetHouse.xpath('./div/@fwid').extract_first())
                        monitorhousebaseitem['HouseFwid'] = HouseFwid
                        HouseLpid = check_data_str(GetHouse.xpath('./div/@lpid').extract_first())
                        monitorhousebaseitem['HouseLpid'] = HouseLpid
                        HouseInfoUrl = 'http://www.wxhouse.com:9097/wwzs/queryYsfwInfo.action?tplYsfw.id=%s&tplYsfw.lpid=%s' % (
                            HouseFwid, HouseLpid)
                        monitorhousebaseitem['HouseInfoUrl'] = HouseInfoUrl
                        monitorhousebaseitem['SourceUrl'] = response.url
                        headers = self.headers
                        headers['Referer'] = response.url
                        result.append(monitorhousebaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerDeveloperBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'no-cache',
            'Connection': 'keep - alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.wxhouse.com:9097',
        }
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'DeveloperBase':
            Developerbaseitem = DeveloperBaseItem()
            Developerbaseitem['SourceUrl'] = response.url

            ProjectName = response.meta.get('ProjectName')

            DeveloperName = check_data_str(
                Selector(response).xpath('/html/body/div/div[3]/div[2]/table/tr[1]/td/b/text()').extract_first())
            Developerbaseitem['DeveloperName'] = DeveloperName
            logging.debug('DeveloperName' + DeveloperName)

            DeveloperAddress = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[5]/td[2]/text()').extract_first())
            Developerbaseitem['DeveloperAddress'] = DeveloperAddress
            logging.debug('DeveloperAddress' + DeveloperAddress)

            DeveloperFullName = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[1]/td[2]/text()').extract_first())
            Developerbaseitem['DeveloperFullName'] = DeveloperFullName
            logging.debug('DeveloperFullName' + DeveloperFullName)

            DeveloperLevel = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Developerbaseitem['DeveloperLevel'] = DeveloperLevel
            logging.debug('DeveloperLevel' + DeveloperLevel)

            LegalPerson = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[3]/td[2]/text()').extract_first())
            Developerbaseitem['LegalPerson'] = LegalPerson
            logging.debug('LegalPerson' + LegalPerson)

            SalesManager = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[4]/td[2]/text()').extract_first())
            Developerbaseitem['SalesManager'] = SalesManager
            logging.debug('SalesManager' + SalesManager)

            ZipCode = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[6]/td[2]/text()').extract_first())
            Developerbaseitem['ZipCode'] = ZipCode
            logging.debug('ZipCode' + ZipCode)

            Fax = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[7]/td[2]/text()').extract_first())
            Developerbaseitem['Fax'] = Fax
            logging.debug('Fax' + Fax)

            Web = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[8]/td[2]/text()').extract_first())
            Developerbaseitem['Web'] = Web
            logging.debug('Web' + Web)

            EMail = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[9]/td[2]/text()').extract_first())
            Developerbaseitem['EMail'] = EMail
            logging.debug('EMail' + EMail)

            DeveloperNo = uuid.uuid3(uuid.NAMESPACE_DNS, DeveloperFullName + DeveloperAddress).hex

            Developerbaseitem['DeveloperNo'] = DeveloperNo

            Developerbaseitem['ProjectName'] = ProjectName

            result.append(Developerbaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return



class SpiderMiddlerHouseBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'HouseBase':
            logging.debug("HouseBase")
            ProjectName = response.meta.get('ProjectName')
            BuildingNum = response.meta.get('BuildingNum')
            HouseNo = response.meta.get('houseNo')

            Housebaseitem = HouseBaseItem()

            Housebaseitem['SourceUrl'] = response.url

            Housebaseitem['ProjectName'] = ProjectName
            logging.debug(ProjectName)

            Housebaseitem['BuildingNum'] = BuildingNum
            logging.debug(BuildingNum)

            Housebaseitem['HouseNo'] = HouseNo
            logging.debug(HouseNo)

            HouseAddress = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[3]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Housebaseitem['HouseAddress'] = HouseAddress
            logging.debug(HouseAddress)

            HouseCode = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[3]/div[2]/table/tr[1]/td[2]/text()').extract_first())
            Housebaseitem['HouseCode'] = HouseCode
            logging.debug(HouseCode)

            HouseSts = check_data_str(
                Selector(response).xpath('/html/body/div[1]/div[6]/div[2]/span/text()').extract_first())
            Housebaseitem['HouseSts'] = HouseSts
            logging.debug(HouseSts)

            BuildingNumber = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Housebaseitem['BuildingNumber'] = BuildingNumber
            logging.debug(BuildingNumber)

            UnitNumber = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[3]/td[2]/text()').extract_first())
            Housebaseitem['UnitNumber'] = UnitNumber
            logging.debug(UnitNumber)

            HouseNumber = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[4]/td[2]/text()').extract_first())
            Housebaseitem['HouseNumber'] = HouseNumber
            logging.debug(HouseNumber)

            ActualFloor = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[5]/td[2]/text()').extract_first())
            Housebaseitem['ActualFloor'] = ActualFloor
            logging.debug(ActualFloor)

            TotalFloor = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[6]/td[2]/text()').extract_first())
            Housebaseitem['TotalFloor'] = TotalFloor
            logging.debug(TotalFloor)

            BuildingStructure = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[7]/td[2]/text()').extract_first())
            Housebaseitem['BuildingStructure'] = BuildingStructure
            logging.debug(BuildingStructure)

            HouseType = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[8]/td[2]/text()').extract_first())
            Housebaseitem['HouseUseType'] = HouseType
            logging.debug(HouseType)

            HouseUseType = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[9]/td[2]/text()').extract_first())
            Housebaseitem['HouseUseType'] = HouseUseType
            logging.debug(HouseUseType)

            AreasType = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[10]/td[2]/text()').extract_first())
            Housebaseitem['AreasType'] = AreasType
            logging.debug(AreasType)

            TotalArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[11]/td[2]/text()').extract_first())
            Housebaseitem['TotalArea'] = TotalArea
            logging.debug(TotalArea)

            InsideOfBuildingArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[12]/td[2]/text()').extract_first())
            Housebaseitem['InsideOfBuildingArea'] = InsideOfBuildingArea
            logging.debug(InsideOfBuildingArea)

            MeasuredSharedPublicArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[13]/td[2]/text()').extract_first())
            Housebaseitem['MeasuredSharedPublicArea'] = MeasuredSharedPublicArea
            logging.debug(MeasuredSharedPublicArea)

            hightArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[14]/td[2]/text()').extract_first())
            Housebaseitem['hightArea'] = hightArea
            logging.debug('hightArea' + hightArea)

            Remarks = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[15]/td[2]/text()').extract_first())
            Housebaseitem['Remarks'] = Remarks
            logging.debug(Remarks)

            Price = check_data_num(
                Selector(response).xpath('/html/body/div[1]/div[5]/div[2]/span/text()').extract_first())
            Housebaseitem['Price'] = Price
            logging.debug(Price)
            if HouseSts:
                result.append(Housebaseitem)
        return result
    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
