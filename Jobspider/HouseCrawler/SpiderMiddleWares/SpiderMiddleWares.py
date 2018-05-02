#!/usr/python3
# -*- coding: utf-8 -*-
import sys
import json
import re
import logging
import random
from scrapy import Request
from scrapy import Selector
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
            'x-requested-with': "XMLHttpRequest",
            'referer': "https://www.zhipin.com/",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'cache-control': "no-cache",
        }

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'GetCitys':
            logging.debug("GetCitys")
            headers = self.headers
            json_data = json.loads(response.body_as_unicode())
            resmsg = json_data.get('resmsg')
            if resmsg == '请求成功':
                data = json_data.get('data')
                for cityList in data.get('cityList',[]):
                    for subLevelModelList in cityList.get('subLevelModelList',[]):
                        code = subLevelModelList.get('code', '')
                        name = subLevelModelList.get('code', '')
                        cityurl = 'https://www.zhipin.com/job_detail/?query=&scity={}&industry=&position='.format(code)
                        print(cityurl)
                        result.append(Request(url=cityurl,
                                              headers=headers,
                                              method='GET',
                                              meta={
                                                  'PageType': 'CityJobs',
                                              }))


        if response.meta.get('PageType') == 'CityJobs':
            logging.debug("CityJobs")
            list_page = Selector(response).xpath('//*[@id="main"]/div/div[2]/div[2]/a')
            havenext = list_page[-1].xpath('./@class').extract_first()
            jobdatas = Selector(response).xpath('//*[@id="main"]/div/div[2]/ul/li')
            for jobdata in jobdatas:
                # job_title://*[@id="main"]/div/div[2]/ul/li[2]/div/div[1]/h3/a/div[1]
                job_title = jobdata.xpath('./div/div[1]/h3/a/div[1]/text()').extract_first()
                print(job_title)

                # pay://*[@id="main"]/div/div[2]/ul/li[28]/div/div[1]/h3/a/span
                pay = jobdata.xpath('./div/div[1]/h3/a/span/text()').extract_first()
                print(pay)

                region = jobdata.xpath('./div/div[1]/p/text()[1]').extract_first()
                print(region)
                workyears = jobdata.xpath('./div/div[1]/p/text()[2]').extract_first()
                print(workyears)
                education = jobdata.xpath('./div/div[1]/p/text()[3]').extract_first()
                print(education)

                industry = jobdata.xpath('./div/div[2]/div/p/text()[1]').extract_first()
                print(industry)
                financing = jobdata.xpath('./div/div[2]/div/p/text()[2]').extract_first()
                print(financing)
                people = jobdata.xpath('./div/div[2]/div/p/text()[3]').extract_first()
                print(people)


                # company://*[@id="main"]/div/div[2]/ul/li[28]/div/div[2]/div/h3/a
                company = jobdata.xpath('./div/div[2]/div/h3/a/text()').extract_first()
                print(company)
                company_url = jobdata.xpath('./div/div[2]/div/h3/a/@href').extract_first()
                print(company_url)

                # pay://*[@id="main"]/div/div[2]/ul/li[28]/div/div[1]/h3/a/span
                pay = jobdata.xpath('./div/div[1]/h3/a/span/text()').extract_first()
                print(pay)

                # pay://*[@id="main"]/div/div[2]/ul/li[28]/div/div[1]/h3/a/span
                publisher = jobdata.xpath('./div/div[3]/h3/text()[1]').extract_first()
                print(publisher)
                publisher_position = jobdata.xpath('./div/div[3]/h3/text()[2]').extract_first()
                print(publisher_position)
                release_time = jobdata.xpath('./div/div[3]/p/text()').extract_first()
                print(release_time)
            print(havenext)
            if havenext == 'next':
                href = list_page[-1].xpath('./@href').extract_first()
                urlnext = 'https://www.zhipin.com' + href + '&ka=page-next'
                result.append(Request(url=urlnext,
                                      method='GET',
                                      meta={
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
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep - alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.wxhouse.com:9097',
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
        if not (200 <= response.status < 300):  # common case
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
                BuildingNum = (buildingTable.xpath('./a/text()').extract_first())
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

                    result.append(Request(url=houseDetailsUrl,
                                          headers=headers,
                                          method='GET',
                                          meta={
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
                HouseClass = (GetHouse.xpath('./@class').extract_first())
                if HouseClass == 'LPBFW_BOROR':
                    monitorhousebaseitem = MonitorHouseBaseItem()
                    monitorhousebaseitem['ProjectName'] = ProjectName
                    monitorhousebaseitem['BuildingNum'] = BuildingNum
                    HouseTitle = (GetHouse.xpath('./@title').extract_first())
                    monitorhousebaseitem['HouseTitle'] = HouseTitle

                    HouseNo = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectName + BuildingNum + str(HouseTitle) + str(num)).hex
                    monitorhousebaseitem['HouseNo'] = HouseNo
                    num = num + 1
                    GetHouseSts = (GetHouse.xpath('./div/@style').extract_first())
                    if GetHouseSts:
                        HouseSts = get_house_sts(GetHouseSts)
                        monitorhousebaseitem['HouseSts'] = HouseSts
                        HouseFwid = (GetHouse.xpath('./div/@fwid').extract_first())
                        monitorhousebaseitem['HouseFwid'] = HouseFwid
                        HouseLpid = (GetHouse.xpath('./div/@lpid').extract_first())
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
