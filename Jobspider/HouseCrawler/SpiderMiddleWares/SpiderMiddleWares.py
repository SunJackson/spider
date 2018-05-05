#!/usr/python3
# -*- coding: utf-8 -*-
import sys
import json
import logging
from datetime import date
import datetime
import re
import uuid
import copy
from redis import Redis
from scrapy import Request
from scrapy import Selector
from Items.Items import JobBaseItem

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
'''
    Created on 2017-11-29 12:44:32.
'''


def clean_data_str(string):
    result_data = string
    if string:
        result_data = string.strip()
        fix_data = {'\r': '', '\n': '', '\t': '','</span>': '','\\': '',
                     ' ': '','<span>': '','<br></span>': '','<br>': '',
                    '<br/>':''
                    }
        for r in fix_data:
            result_data = result_data.strip().replace(r, fix_data[r])
    return result_data


class SpiderMiddlerGetJsonDate(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.r = Redis(host='127.0.0.1', port='6379')
        self.year = str(date.today().year)
        self.month = str(date.today().month)
        self.day = str(date.today().day)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def release_time_clean(data):
            if data == '':
                return data
            else:
                if ':' in data:
                    datatime = datetime.date.today().strftime("%Y-%m-%d ") + data
                elif '月' in data:
                    datatime = self.year + '-' + data.replace('月', '-').replace('日', ' ') + '12:00'
                elif '昨天' in data:
                    datatime = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M")
                return datatime

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'GetCitys':
            logging.debug("GetCitys")
            headers = {
                'accept': "application/json, text/javascript, */*; q=0.01",
                'x-requested-with': "XMLHttpRequest",
                'referer': response.url,
                'accept-encoding': "gzip, deflate, br",
                'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                'cache-control': "no-cache",
            }
            print(response.body_as_unicode())
            json_data = json.loads(response.body_as_unicode())
            resmsg = json_data.get('resmsg')
            if resmsg == '请求成功':
                data = json_data.get('data')
                for cityList in data.get('cityList', []):
                    for subLevelModelList in cityList.get('subLevelModelList', []):
                        code = subLevelModelList.get('code', '')
                        name = subLevelModelList.get('name', '')
                        cityurl = 'https://www.zhipin.com/job_detail/?query=&scity={}&industry=&position='.format(code)
                        print(cityurl)
                        # result.append(Request(url=cityurl,
                        #                       headers=headers,
                        #                       method='GET',
                        #                       meta={
                        #                           'PageType': 'CityJobs',
                        #                       }))
                        city_base = {
                            'source_url': cityurl,
                            'headers': headers,
                            'method': 'GET',
                            'meta': {
                                'PageType': 'CityJobs',
                                'CityCode': code,
                                'CityName': name
                            }}
                        base_json = json.dumps(city_base, sort_keys=True)
                        self.r.sadd('BossSpider', base_json)

        if response.meta.get('PageType') == 'CityJobs':
            logging.debug("CityJobs")
            havenext = ''
            CityCode = str(response.meta.get('CityCode'))
            CityName = str(response.meta.get('CityName'))
            list_page = Selector(response).xpath('//*[@id="main"]/div/div[2]/div[2]/a')
            '//*[@id="main"]/div/div[2]/div[2]/a[6]'
            if list_page:
                havenext = list_page[-1].xpath('./@class').extract_first()
            jobdatas = Selector(response).xpath('//*[@id="main"]/div/div[2]/ul/li')
            for jobdata in jobdatas:
                DataItem = JobBaseItem()
                DataItem['CityCode'] = CityCode
                DataItem['CityName'] = CityName
                job_title = jobdata.xpath('./div/div[1]/h3/a/div[1]/text()').extract_first()
                DataItem['JobTitle'] = job_title
                pay = jobdata.xpath('./div/div[1]/h3/a/span/text()').extract_first()
                DataItem['Pay'] = pay
                region = jobdata.xpath('./div/div[1]/p/text()[1]').extract_first()
                DataItem['Region'] = region
                workyears = jobdata.xpath('./div/div[1]/p/text()[2]').extract_first()
                DataItem['WorkYears'] = workyears
                education = jobdata.xpath('./div/div[1]/p/text()[3]').extract_first()
                DataItem['Education'] = education
                industry = jobdata.xpath('./div/div[2]/div/p/text()[1]').extract_first()
                DataItem['Industry'] = industry
                financing = jobdata.xpath('./div/div[2]/div/p/text()[2]').extract_first()
                DataItem['Financing'] = financing
                people = jobdata.xpath('./div/div[2]/div/p/text()[3]').extract_first()
                DataItem['People'] = people
                company = jobdata.xpath('./div/div[2]/div/h3/a/text()').extract_first()
                DataItem['Company'] = company
                company_url = jobdata.xpath('./div/div[2]/div/h3/a/@href').extract_first()
                DataItem['CompanyUrl'] = 'https://www.zhipin.com/' + company_url
                publisher = jobdata.xpath('./div/div[3]/h3/text()[1]').extract_first()
                DataItem['Publisher'] = publisher
                publisher_position = jobdata.xpath('./div/div[3]/h3/text()[2]').extract_first()
                DataItem['PublisherPosition'] = publisher_position
                release_time = jobdata.xpath('./div/div[3]/p/text()').extract_first().replace('发布于', '')
                DataItem['ReleaseTime'] = release_time_clean(release_time)
                ka = jobdata.xpath('./div/div[1]/h3/a/@ka').extract_first()
                DataItem['Ka'] = ka
                data_jid = jobdata.xpath('./div/div[1]/h3/a/@data-jid').extract_first()
                DataItem['DataJid'] = data_jid
                data_lid = jobdata.xpath('./div/div[1]/h3/a/@data-lid').extract_first()
                DataItem['DataLid'] = data_lid

                DataItem['JobUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                 job_title +
                                                 region +
                                                 CityCode
                                                 ).hex

                headers = {
                    'accept': "application/json, text/javascript, */*; q=0.01",
                    'x-requested-with': "XMLHttpRequest",
                    'referer': response.url,
                    'accept-encoding': "gzip, deflate, br",
                    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    'cache-control': "no-cache",
                }
                job_detail_url = 'https://www.zhipin.com/job_detail/{}.html?ka={}&lid={}'.format(data_jid, ka, data_lid)
                # job_detail_url = 'https://www.zhipin.com/view/job/card.json?jid={}&lid={}'.format(data_jid, data_lid)
                result.append(Request(url=job_detail_url,
                                      headers=headers,
                                      method='GET',
                                      meta={
                                          'PageType': 'JobDetail',
                                          'item': DataItem
                                      }))
                # job_base = {
                #     'source_url': job_detail_url,
                #     'headers': headers,
                #     'method': 'GET',
                #     'meta': {
                #         'PageType': 'JobDetail',
                #         'item':
                #     }}
                # base_json = json.dumps(job_base, sort_keys=True)
                # self.r.sadd('Spider', base_json)
            if havenext == 'next':
                href = list_page[-1].xpath('./@href').extract_first()
                urlnext = 'https://www.zhipin.com' + href + '&ka=page-next'
                # result.append(Request(url=urlnext,
                #                       method='GET',
                #                       meta={
                #                           'PageType': 'CityJobs',
                #                       }))
                job_base = {
                    'source_url': urlnext,
                    'method': 'GET',
                    'meta': {
                        'PageType': 'CityJobs',
                    }}
                base_json = json.dumps(job_base, sort_keys=True)
                self.r.sadd('BossSpider', base_json)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerJobDetail(object):
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
        def detail_clean(data):
            details = str(data)
            detail = re.search('<div class="detail-bottom-text">(.*?)</div>', data)
            if detail:
                details = ';'.join(detail.group(0).split('<br/>')[1:-1])
            return details

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'JobDetail':
            logging.debug("JobDetail")
            JobDataitem = response.meta.get('item')
            JobDataItem = copy.deepcopy(JobDataitem)
            JobDetail = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div/text()').extract_first()
            JobDataItem['JobDetail'] = clean_data_str(JobDetail)

            CompanyDetail = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[2]/div/text()').extract_first()
            JobDataItem['CompanyDetail'] = clean_data_str(CompanyDetail)

            CompanyName = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[3]/div[1]/text()').extract_first()
            JobDataItem['CompanyName'] = clean_data_str(CompanyName)

            LegalRepresentative = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[3]/div[2]/li[1]/text()').extract_first()
            JobDataItem['LegalRepresentative'] = clean_data_str(LegalRepresentative)

            RegisteredCapital = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[3]/div[2]/li[2]/text()').extract_first()
            JobDataItem['RegisteredCapital'] = clean_data_str(RegisteredCapital)

            ResTime = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[3]/div[2]/li[3]/text()').extract_first()
            JobDataItem['ResTime'] = clean_data_str(ResTime)

            CompanyType = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[3]/div[2]/li[4]/text()').extract_first()
            JobDataItem['CompanyType'] = clean_data_str(CompanyType)

            ManageState = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[3]/div[2]/li[5]/text()').extract_first()
            JobDataItem['ManageState'] = clean_data_str(ManageState)

            LoactionAddress = Selector(response).xpath(
                '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[4]/div/div[1]/text()').extract_first()
            JobDataItem['LoactionAddress'] = clean_data_str(LoactionAddress)

            result.append(JobDataItem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
