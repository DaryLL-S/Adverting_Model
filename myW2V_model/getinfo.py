import pymongo
import csv
import re

head = ['_key', 'username', 'location', 'postcount', 'likes', 'post', 'gender', 'identity', 'marriage', 'region',
            'risk_appetite', 'education', 'revenue', 'deposit', 'debt', 'intended_products', 'label']

def connect_mongo():
    client = pymongo.MongoClient(host='119.29.80.39', port=27017)
    db = client.get_database('nodebb')
    db.authenticate("spititout", "SWIFTspititout2021")
    collection = db.get_collection("objects")
    return collection


def userinfo(collection):
    with open("./data/initial_data.csv", 'w', encoding='utf-8', newline='') as wf:
        wiriter = csv.DictWriter(wf, fieldnames=head)
        wiriter.writeheader()
        result = collection.find({'_key': 'global'})
        for index, info in enumerate(result):
            userCount = info.get('userCount')
        for i in range(userCount + 1):
            result1 = collection.find({'_key': f'user:{i}'})
            temp = dict()
            for index, info in enumerate(result1):
                temp['_key'] = info.get('_key')
                temp['_key'] = re.sub(r"user:", '', temp['_key'])
                temp['username'] = info.get('username')
                temp['location'] = info.get('location')
                temp['postcount'] = info.get('postcount')
                temp['likes'] = info.get('reputation')

            i = float(i)
            result2 = collection.find({"uid": i, "_key": {'$regex': 'post:.*'}})
            temp['post'] = []
            for index, info in enumerate(result2):
                temp['post'].append(info.get('content'))
            wiriter.writerow(
                {'_key': temp['_key'], 'username': temp['username'], 'location': temp['location'],
                 'postcount': temp['postcount'], 'likes': temp['likes'], 'post': temp['post']})


def merge_data():
    with open("./data/full_data.csv", 'w', encoding='utf-8', newline='') as wf:
        i = 0
        wiriter = csv.DictWriter(wf, fieldnames=head)
        wiriter.writeheader()
        with open("./data/initial_data.csv", 'r', encoding='utf-8', newline='') as rf1:
            reader1 = csv.DictReader(rf1)
            for row in reader1:
                temp = dict()
                temp['_key'] = i
                temp['username'] = row['username']
                temp['location'] = row['location']
                temp['postcount'] = row['postcount']
                temp['likes'] = row['likes']
                temp['post'] = row['post']

                wiriter.writerow(
                    {'_key': temp['_key'], 'username': temp['username'], 'location': temp['location'],
                     'postcount': temp['postcount'], 'likes': temp['likes'], 'post': temp['post']})
                i = i + 1

        with open("./data/extra_data.csv", 'r', encoding='utf-8', newline='') as rf2:
            reader2 = csv.DictReader(rf2)
            for row in reader2:
                temp = dict()
                temp['_key'] = i
                temp['username'] = row['username']
                temp['location'] = row['location']
                temp['postcount'] = row['postcount']
                temp['likes'] = row['likes']
                temp['post'] = row['post']

                wiriter.writerow(
                    {'_key': temp['_key'], 'username': temp['username'], 'location': temp['location'],
                     'postcount': temp['postcount'], 'likes': temp['likes'], 'post': temp['post']})
                i = i + 1
