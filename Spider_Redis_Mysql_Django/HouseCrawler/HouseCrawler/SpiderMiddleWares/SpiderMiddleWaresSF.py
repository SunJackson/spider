# -*- coding: utf-8 -*-
import datetime

import regex
from HouseCrawler.Items.item import RACoordinateItem, ResidentialAreaItem
from scrapy import Request, Selector


class BaseSpiderMiddleWare(object):
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Host': 'esf.gz.fang.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://gz.fang.com/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    @staticmethod
    def process_spider_exception(response, exception, spider):
        return


class RAListHandleMiddleware(BaseSpiderMiddleWare):
    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):    # common case
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('RAList', 'RAInfo' ):
            if result:
                return result
            return []
        print('RAListHandleMiddleware')
        sel = Selector(text=response.body_as_unicode())
        if response.meta.get('PageType') == 'RAList':
            _pages = sel.xpath(
                '//*[@id="houselist_B14_01"]/span/text()').extract_first()
            _pages = regex.search(r'共(.*?)页', _pages)
            if _pages:
                pgs = int(_pages.groups(0)[0])
                area_name = response.meta.get('RA')
                area_num = response.meta.get('RANum')
                req_list = list()
                for i in range(1, pgs + 1):
                    area_list_id = '{RA}__0_0_0_0_{Page}_0_0_0'.format(
                        RA=area_num, Page=i)
                    area_list_url = 'http://esf.gz.fang.com/housing/{}'.format(
                        area_list_id)
                    meta_pack = {
                        'PageType': 'RAInfo',
                        'RA': area_name,
                        'RANum': area_num
                    }

                    r = Request(area_list_url, meta=meta_pack, headers=self.headers)
                    req_list.append(r)
                result.extend(req_list)

        elif response.meta.get('PageType') == 'RAInfo':
            print('----------------------RAInfo')
            _urls = sel.xpath('//*[@class="houseList"]/div[@class="list rel"]'
                              '/dl/dd/p/a[@class="plotTit"]/@href')
            if _urls:
                req_list = list()
                for i, url in enumerate(_urls.extract()):
                    if 'http' in url:
                        xq_url = url + 'xiangqing/'
                        r = Request(
                            xq_url,
                            meta={
                                'PageType': 'RADetail',
                                'RA': response.meta.get('area_name', ''),
                                'URL': url
                            }, headers=self.headers)
                        req_list.append(r)
                result.extend(req_list)
        return result


class RADetailHandleMiddleware(BaseSpiderMiddleWare):
    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):    # common case
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('RADetail', ):
            if result:
                return result
            return []
        print('RADetailHandleMiddleware')
        sel = Selector(text=response.body_as_unicode())
        if response.meta.get('PageType') == 'RADetail':
            RAName = sel.xpath('//div[@class="ceninfo_sq"]'
                               '/h1/a[@class="tt"]/text()').extract_first()
            if RAName:
                # Name Info
                nt = datetime.datetime.now()
                info_pack = sel.xpath('//div[@class="inforwrap clearfix"]/'
                                      'dl[@class=" clearfix mr30"]/dd')
                info_index = self.index_constructor(info_pack)
                item = ResidentialAreaItem()
                item['CreatedDate'] = nt
                item['ManagementFees'] = info_index.get('物业费', '').replace(
                    '元/㎡·月', '')
                item['ManagementCompany'] = info_index.get('物业公司', '')
                item['GreeningRate'] = info_index.get('绿化率', '').strip('%')
                _rn = info_index.get('所属区域', '').split(' ')
                item['RegionName'] = _rn[
                    1] if len(_rn) is 2 else info_index.get('所属区域', '')
                item['FloorAreaRatio'] = info_index.get('容积率', '')
                item['DistrictName'] = response.meta.get('RA', '')
                item['Address'] = info_index.get('小区地址', '')
                item['ResidentialAreaName'] = RAName
                item['DeveloperCompany'] = info_index.get('开发商', '')
                item['HouseBuildingCount'] = info_index.get('楼栋总数',
                                                            '').strip('户')
                item['HousingCount'] = info_index.get('总户数', '').strip('栋')
                item['BuildingArea'] = info_index.get('建筑面积', '').replace(
                    '平方米', '')
                item['LandArea'] = info_index.get('占地面积', '').replace(
                    '平方米', '')
                item['BuildingCategorys'] = info_index.get('建筑类型', '')
                item['LandUseYearsLimitDescribe'] = info_index.get('产权描述', '')
                item['CompletionDate'] = info_index.get('建筑年代', '')
                # History Sell Record
                sell_pack = sel.xpath('//div[@class="inforwrap clearfix"]/'
                                      'dl[@class="mr30 clearfix"]/dd')
                sell_index = self.index_constructor(sell_pack)
                item['SellDate'] = sell_index.get('开盘时间', '')
                item['SaleStatus'] = '二手'
                # Others
                other_pack = sel.xpath('//div[@class="box"]')
                other_index = self.index_for_text_constructor(other_pack)
                item['TrafficInfo'] = other_index.get('交通状况', '')
                item['PeripheralSupporting'] = other_index.get('周边信息', '')
                item['URLID'] = response.meta.get('URL')
                result.append(item)
                map_info_url = sel.xpath(
                    '//iframe[@id=""]/@src').extract_first()

                if map_info_url:
                    r = Request(
                        map_info_url,
                        meta={
                            'PageType': 'MapInfo',
                            'URL': response.meta.get('URL'),
                            'NowTime': nt
                        }, headers=self.headers)
                    result.append(r)
        return result

    @staticmethod
    def index_constructor(pack):
        result = {}
        for i, p in enumerate(pack):
            key = p.xpath('./strong/text()').extract_first() or ''
            key = key.strip('：').replace(' ', '').replace('\xa0', '')
            val = p.xpath('./text()').extract_first() or ''
            attr = p.xpath('./@title').extract_first() or ''
            result[key] = val.strip()
            if attr:
                result[key] = attr.strip()
        return result

    @staticmethod
    def index_for_text_constructor(pack):
        result = {}
        # taps = ['交通状况', '周边信息', '地理位置']
        taps = ['交通状况', '周边信息']
        for i, p in enumerate(pack):
            title = p.xpath(
                './div[@class="box_tit"]/h3/text()').extract_first() or ''
            if title in taps:
                text = p.xpath('./div[@class="inforwrap clearfix"]'
                               '/dl[@class="floatl mr30"]/dt/text()')
                text = ''.join([
                    t.replace('\r', '').replace('\n', '').replace('；', '')
                    for t in text.extract()
                ])
                result[title] = text
        return result


class RACoordnateHandleMiddleware(BaseSpiderMiddleWare):
    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):    # common case
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('MapInfo', ):
            if result:
                return result
            return []

        sel = Selector(text=response.body_as_unicode())
        if response.meta.get('PageType') == 'MapInfo':
            div = sel.xpath(
                '//script[re:test(text(), "mapInfo=(.*?)")]/text()')
            content = div.extract_first() or ''
            content = regex.search(r'mapInfo={(.*?)};', content)
            if content:
                content = content.groups()[0]
                try:
                    ix = {}
                    for pair in content.split(','):
                        k, v = pair.split(':')
                        ix[k.strip()] = v.strip()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                else:
                    item = RACoordinateItem()
                    item['URLID'] = response.meta.get('URL', '')
                    item['CreatedDate'] = response.meta.get('NowTime', '')
                    item['MapType'] = '百度地图'
                    item['XLongitude'] = float(ix.get('px').replace('"', ''))
                    item['YLatitude'] = float(ix.get('py').replace('"', ''))
                    item['XYCoordinateArray'] = '{x},{y}'.format(
                        x=item['XLongitude'], y=item['YLatitude'])
                    result.append(item)
        return result
