# coding = utf-8
import json
import redis
import random
import psycopg2
from cells.net import add_url_params

r = redis.Redis(host='10.30.1.18', port=6379)

def loadBaseUrl():
    conn = psycopg2.connect(database='fang', user='root', password='gh001', host='10.30.4.68', port='5432')
    cur = conn.cursor()
    cur.execute("select source_url from seed_esf_ajk_abzzqzzzz_fafeccc3")
    rows = cur.fetchall()

    for row in rows:
        print(row)
        starurl = row[0]
        project_base = {'source_url': starurl, 'meta': {}}
        project_base_json = json.dumps(project_base, sort_keys=True)
        r.sadd('IpCrawler', project_base_json)

def loadJson():
    with open("./urls.json", 'r') as load_f:
        load_dict = json.load(load_f)
    num = 0
    for row in load_dict:
        print(row)
        starurl = row
        payload = {'url': row, 'proxy_level': 'high'}

        project_base = {'source_url': starurl, 'meta': {}}
        project_base_json = json.dumps(project_base, sort_keys=True)
        r.sadd('IpCrawler', project_base_json)
        if num > 1000:
            break
        num += 1


if __name__ == "__main__":
    loadJson()

# r = redis.Redis(host='10.30.1.18', port=6379)
# r = redis.Redis(host='127.0.0.1', port=6379)
#
# starurl = 'http://www.fangdi.com.cn/House.asp?ProjectID=OTk4N3wyMDE3LTEyLTF8NjM=&projectName=%C8%DA%D0%C5%B2%AC%C6%B7%D1%C5%D6%FE&PreSell_ID=19701&Start_ID=19589&bname=%C7%E0%C6%D6%C7%F8%D3%AF%C6%D6%BD%D6%B5%C0%B4%F3%D3%AF%C6%D6%C2%B71500%C5%AA7%BA%C5&Param=MjUwMzg0MTUyNXx8MjAxNy0xMi0xIDExOjM2OjA5fHw3NA==&flag=MQ=='
# project_base = {
#                     'source_url': starurl,
#                     "meta": {
#         "PageType": "HouseBase",
#         "building_no": "d247ce961d5932c9938d8cd244e699b9",
#         "opening_unit_no": "019647",
#         "shprojectuuid": "ebd0322c0e8033d79462d9b47a8873f0"
#     }
# }
# project_base_json = json.dumps(project_base, sort_keys=True)
# r.sadd('ShanghaiCrawler:start_urls', project_base_json)
