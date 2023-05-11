from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


class ElasticSearch:
    def __init__(self, host='localhost', port=9200):
        self.client = Elasticsearch([{'host': host, 'port': port}])

    def search(self, index, query):
        s = Search(using=self.client, index=index)
        q = Q('query_string', query=query)
        s = s.query(q)
        response = s.execute()
        return response.to_dict()

    def index(self, index, document, id=None):
        self.client.index(index=index, document=document, id=id)

    def delete_index(self, index):
        self.client.indices.delete(index=index)

    def create_index(self, index, body):
        self.client.indices.create(index=index, body=body)

    def index_exists(self, index):
        return self.client.indices.exists(index=index)


es = ElasticSearch()

# 创建索引
index = 'new_index'

body = {
    'mappings': {'properties': {'title': {'type': 'text'}, 'body': {'type': 'text'}}}
}
es.create_index(index, body)

# 检查索引是否存在
if es.index_exists(index):
    print(f"{index} exists")

# 将文档添加到索引中
doc = {'title': 'Example Document', 'body': 'This is an example document.'}
es.index(index, doc)

# 搜索文档
query = 'example'
response = es.search(index, query)
print(response)
# 删除索引
es.delete_index(index)
