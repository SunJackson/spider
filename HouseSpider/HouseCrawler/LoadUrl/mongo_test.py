from pymongo import MongoClient
client = MongoClient('10.30.1.2', 27017)
mongodb = client['NewHouse_shanghai']


def find_latest_one(table_name, query):
    sort_data = [('CurTimeStamp', -1)]
    cursor = mongodb[table_name].find_one(query, sort=sort_data)
    print(cursor)
    return cursor


def find_latest_one_update(table_name, query, update):
    sort_data = [('CurTimeStamp', -1)]
    mongodb[table_name].find_one_and_update(query, update=update, sort=sort_data)


result = find_latest_one('building_base_shanghai', {"project_no": "a31280sf5d8ca39768a40d21311e289fa"})
# find_latest_one_update('building_base_shanghai', {"project_no": "a31280f5d8ca39768a40d21311e289fa"}, {'$set': {"CurTimeStamp": "2018-05-15 19:27:33.867415"}})
# print(result['CurTimeStamp'])