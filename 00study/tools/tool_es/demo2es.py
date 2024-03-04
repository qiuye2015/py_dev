import json
import sys

import elasticsearch
from elasticsearch import Elasticsearch
from loguru import logger

# Initialize the Elasticsearch client
# allow up to 25 connections to each node
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], maxsize=25)
print(json.dumps(es.info()))

# Define the index name
index_name = 'my_index'


# Create an index
def create_index():
    # def create(self, index, body=None, params=None, headers=None):
    r = es.indices.create(index=index_name, ignore=400)  # ignore 400 already exists code
    logger.trace(json.dumps(r))


# Add a document to the index
def add_document(doc_id, document):
    r = es.index(index=index_name, id=doc_id, document=document, filter_path=['_index', '_id', 'result'])
    logger.trace(r)


# Get a document from the index
def get_document(doc_id):
    try:
        # result = es.get(index=index_name, id=doc_id, ignore=404)
        result = es.get(index=index_name, id=doc_id)
        return result.get('_source')
    except elasticsearch.NotFoundError as e:
        logger.trace(e)
        raise e


# Update a document in the index
def update_document(doc_id, updated_document):
    r = es.index(index=index_name, id=doc_id, document=updated_document, filter_path=['_index', '_id', 'result'])
    logger.trace(r)


# Delete a document from the index
def delete_document(doc_id):
    try:
        r = es.delete(index=index_name, id=doc_id, ignore=404, filter_path=['_index', '_id', 'result'])
        logger.trace(r)
    except elasticsearch.NotFoundError as e:
        logger.trace(e)
        raise e


def mock_data():
    from elasticsearch import Elasticsearch

    # 连接到 Elasticsearch，确保 Elasticsearch 服务在运行中
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # 创建索引并设置映射（mapping）
    index_name = "your_index_name"  # 替换为实际的索引名称

    mapping = {
        "mappings": {
            "properties": {
                "uuid_all": {
                    "type": "nested",  # 将 uuid_all 字段映射为 nested 类型
                    "properties": {
                        "uuid": {"type": "keyword"},
                        "record_param_type": {"type": "keyword"}
                    }
                },
                "record_type": {"type": "keyword"}
            }
        }
    }

    # 创建索引并设置映射
    es.indices.create(index=index_name, body=mapping, ignore=400)

    # 插入数据到 Elasticsearch
    data_to_insert = {
        "uuid_all": [
            {"uuid": "uuid1", "record_param_type": "light"},
            {"uuid": "uuid2", "record_param_type": "normal"}
        ],
        "record_type": "light"
    }

    # 插入数据到 Elasticsearch
    es.index(index=index_name, body=data_to_insert)

    # 查询数据
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"record_type": "light"}},
                    {"nested": {
                        "path": "uuid_all",
                        "query": {
                            "bool": {
                                "must": [
                                    {"match": {"uuid_all.record_param_type": "normal"}}
                                ]
                            }
                        }
                    }}
                ]
            }
        }
    }

    # 执行查询
    search_result = es.search(index=index_name, body=query)

    # 输出查询结果
    print("Search Results:")
    for hit in search_result['hits']['hits']:
        print(hit['_source'])


def mock_data_2():
    from elasticsearch import Elasticsearch

    # 连接到 Elasticsearch，确保 Elasticsearch 服务在运行中
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # 创建索引并设置映射（mapping）
    index_name = "your_index_name_2"  # 替换为实际的索引名称

    mapping = {
        "mappings": {
            "properties": {
                "uuid_all": {
                    "type": "nested",  # 将 uuid_all 字段映射为 nested 类型
                    "properties": {
                        "uuid": {"type": "keyword"},
                        "record_param_type": {"type": "keyword"}
                    }
                },
                "record_type": {"type": "keyword"}
            }
        }
    }

    # 创建索引并设置映射
    es.indices.create(index=index_name, body=mapping, ignore=400)

    # 插入数据到 Elasticsearch，包含了旧数据和新数据
    data_to_insert = [
        {
            "uuid_all": [
                {"uuid": "uuid1", "record_param_type": "light"},
                {"uuid": "uuid2", "record_param_type": "normal"}
            ],
            "record_type": "light"
        },
        {
            "uuid_all": [
                {"uuid": "uuid3", "record_param_type": "normal"}
            ],
            # 旧数据没有 record_type 字段
        }
    ]

    # # 插入数据到 Elasticsearch
    # for data in data_to_insert:
    #     es.index(index=index_name, body=data)

    # 查询数据，处理旧数据中缺少 record_type 字段的情况
    # query = {
    #     "query": {
    #         "bool": {
    #             "must": [
    #                 {"bool": {"should": [{"exists": {"field": "record_type"}},
    #                                      {"bool": {"must_not": {"exists": {"field": "record_type"}}}}]}},
    #                 {"match": {"record_type": "light"}},
    #             ]
    #         }
    #     }
    # }

    query = {
        "query": {
            "bool": {
                "must_not": [
                    {"match": {"record_type": "normal"}},
                    {"match": {"record_type": "light"}},
                ]
            }
        }
    }

    # 执行查询
    search_result = es.search(index=index_name, body=query)

    # 输出查询结果
    print("Search Results:")
    for hit in search_result['hits']['hits']:
        print(hit['_source'])


if __name__ == "__main__":
    logger.remove()
    # logger.add(sys.stderr, level="DEBUG")
    logger.add(sys.stderr, level="TRACE")

    mock_data_2()
    exit(1)
    create_index()

    document_id = 1
    document = {"title": "Sample Document", "content": "This is a sample document."}
    add_document(document_id, document)

    # Get and print the document
    retrieved_document = get_document(document_id)
    logger.info(f"Retrieved Document:{retrieved_document}")

    # Update the document
    updated_document = {"title": "Updated Document", "content": "This document has been updated."}
    update_document(document_id, updated_document)

    # Get and print the updated document
    updated_document = get_document(document_id)
    logger.info(f"Updated Document:{updated_document}")

    # Delete the document
    delete_document(document_id)
    delete_document(document_id)

    # Try to get the deleted document (should raise an exception)
    try:
        deleted_document = get_document(document_id)
        logger.info(f"Deleted Document:{deleted_document}")
    except Exception as e:
        logger.error(f"Document with ID {document_id} not found:{str(e)}")


