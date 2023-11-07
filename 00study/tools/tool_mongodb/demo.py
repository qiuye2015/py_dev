import json

from pymongo import MongoClient

#
# ## 将处理后的数据写入MongoDB。
# class MongoBase:
#     def __init__(self, collection):
#         self.db = None
#         self.con = None
#         self.collection = collection
#         self.OpenDB()
#
#     def OpenDB(self):
#         user = '******'
#         passwd = '******'
#         host = '******'
#         port = '******'
#         auth_db = '******'
#         uri = "mongodb://" + user + ":" + passwd + "@" + host + ":" + port + "/" + auth_db + ""
#         uri = "mongodb://mongouser:dpjhDNS8MfMj@10.134.218.3:27017,10.134.218.8:27017,10.134.218.4:27017/test?authSource=admin"
#         self.con = MongoClient(uri, connect=False)
#         self.db = self.con[auth_db]
#         self.collection = self.db[self.collection]
#
#     def closeDB(self):
#         self.con.close()
#
#
# mongo = MongoBase('test')
# mongo.collection.insert(json.loads({"test": 1}).values())
# mongo.closeDB()

#
# from pymongo import MongoClient, ASCENDING
#
#
# class MongoUrl:
#     def __init__(self, ip='127.0.0.1', port=27017):
#         conn = MongoClient(ip, port)
#         self.db = conn.News
#         self.collection = self.db.new_url
#         self.collection.create_index([('nid', ASCENDING)])  # TODO:
#
#     def insert(self, item_dict):
#         # 插入数据
#         self.collection.insert_one(item_dict)
#
#     def select_one(self, item_dict):
#         return self.collection.find_one(item_dict)
#
#     def select(self, item_dict):
#         # 自定义选择数据
#         return self.collection.find(item_dict)
#
#     def delete(self, query_dict):
#         self.collection.delete_one(query_dict)
#
#     def delete_all(self, item_dict):
#         #
#         self.collection.delete_many(item_dict)
#
#     def find_one_update_flag1(self):
#         return self.collection.find_one_and_update({"flag": 0}, {'$set': {"flag": 1}})
#
#     def update_url_flag0(self, url):
#         self.collection.update({'url': url}, {'$set': {"flag": 0}})
#
#     def update(self, item_dict):
#         self.collection.update(item_dict)
#
#     def count(self):
#         self.collection.count_documents({})
#
#
# db_mu = MongoUrl()
# db_mu.insert(
#     {"url": "http://www.baidu.com", "time": '2019-05-03 01:32:00', "flag": 0, "title": "暂无", "type": "baidu_new百度新闻"}
# )


from pymongo import MongoClient


class MongoDB:
    def __init__(self, host, port, username=None, password=None, auth_source='admin'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.client = None
        self.db = None

        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                authSource=self.auth_source,
            )
            # self.db = self.client.get_default_database()
            self.db = self.client[self.auth_source]
            print('Connected to MongoDB')
        except Exception as e:
            print(f'Failed to connect to MongoDB: {str(e)}')

    def disconnect(self):
        try:
            if self.client:
                self.client.close()
                self.client = None
                self.db = None
                print('Disconnected from MongoDB')
        except Exception as e:
            print(f'Error while disconnecting from MongoDB: {str(e)}')

    def insert_document(self, collection_name, document):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            print(f'Error while inserting document: {str(e)}')

    def find_documents(self, collection_name, filter=None, projection=None):
        try:
            collection = self.db[collection_name]
            documents = collection.find(filter, projection)
            return list(documents)
        except Exception as e:
            print(f'Error while finding documents: {str(e)}')

    # 添加其他常用操作方法，如更新、删除、索引等


# 示例用法
mongo = MongoDB(host='localhost', port=27017)
# mongo.connect()

# 插入文档
document = {'name': 'John', 'age': 30}
inserted_id = mongo.insert_document('mycollection', document)
print(f'Inserted document with ID: {inserted_id}')

# 查询文档
documents = mongo.find_documents('mycollection', filter={'age': {'$gt': 25}})
for doc in documents:
    print(doc)

# 关闭连接
mongo.disconnect()
