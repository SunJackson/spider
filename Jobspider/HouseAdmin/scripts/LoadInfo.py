# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import redis
import random
from NewWuxi.HouseCrawler.HouseAdmin.HouseNew.models import *

r = redis.Redis(host='10.30.1.18', port=6379)
headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'no-cache',
            'Connection': 'keep - alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.wxhouse.com:9097',
        }
def loadProject():
    cur = MonitorProjectBaseWuxi.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                             {'$group':
                                                 {'_id': "$ProjectNo",
                                                  'CurTimeStamp':{'$last': '$CurTimeStamp'},
                                                  'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                                  'change_data': {'$last': '$change_data'},
                                                  'projectDetailUrl':{'$last': '$projectDetailUrl'},
                                                  'ProjectCode': {'$last': '$ProjectCode'},
                                                 }
                                             }],allowDiskUse=True)

    num = 0
    for item in cur:
        change_data = item['change_data']
        projectDetailUrl = item['projectDetailUrl']
        if projectDetailUrl and change_data != "last" and change_data != "":
            res_object = MonitorProjectBaseWuxi.objects.filter(ProjectNo=item['_id']).latest(field_name='CurTimeStamp')
            res_object.change_data = "last"
            res_object.save()
            ProjectCode = item['ProjectCode']
            projectInfo = {'source_url': item['projectDetailUrl'],
                           'meta': {
                               'PageType': 'ProjectInfo',
                               'ProjectHref': ProjectCode
                           }
                           }
            builfing_info_json = json.dumps(projectInfo, sort_keys=True)
            r.sadd('WuxiCrawler:start_urls', builfing_info_json)
def loadHouse():

    cur = MonitorHouseBaseWuxi.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                                 {'$group':
                                                      {'_id': "$HouseNo",
                                                       'CurTimeStamp': {'$last': '$CurTimeStamp'},
                                                       'NewCurTimeStamp': {'$last': '$NewCurTimeStamp'},
                                                       'change_data': {'$last': '$change_data'},
                                                       'HouseInfoUrl': {'$last': '$HouseInfoUrl'},
                                                       'ProjectName': {'$last': '$ProjectName'},
                                                       'BuildingNum': {'$last': '$BuildingNum'},
                                                       'SourceUrl': {'$last': '$SourceUrl'},
                                                       }
                                                  },
                                              ],allowDiskUse=True)
    for item in cur:
        change_data = item['change_data']
        HouseInfoUrl = item['HouseInfoUrl']
        HouseNo = item['_id']
        ProjectName = item['ProjectName']
        BuildingNum = item['BuildingNum']
        SourceUrl = item['SourceUrl']
        if change_data != "last":
            res_object = MonitorHouseBase.objects.filter(HouseNo=item['_id']).latest(field_name='CurTimeStamp')
            res_object.change_data = "last"
            res_object.save()
            headers['Referer'] = SourceUrl
            projectInfo = {'source_url': HouseInfoUrl,
                           'headers': headers,
                           'method': 'GET',
                           'meta': {
                               'PageType': 'HouseBase',
                               'ProjectName': ProjectName,
                               'BuildingNum': BuildingNum,
                               'houseNo': HouseNo,
                           }
                           }
            project_info_json = json.dumps(projectInfo, sort_keys=True)
            r.sadd('WuxiCrawler:start_urls', project_info_json)
def run():
    loadHouse()
    loadProject()
if __name__ == "__main__":
    run()