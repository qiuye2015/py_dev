from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
import warnings
import es_enum

warnings.filterwarnings("ignore")


def es_open(hosts_):
    # return Elasticsearch(hosts=hosts_,basic_auth=(),verify_certs=False)
    es = Elasticsearch(hosts=hosts_, verify_certs=False)
    print(es.info())
    return es


def es_close(client_):
    client_.close()


def es_create_index(client_, index_="test_fjp"):
    # 定义映射
    mappings = {
        "properties": {
            "num": {"type": "integer"},
            "name": {"type": "text"},
        }
    }
    if client_.indices.exists(index=index_):
        client_.indices.delete(index=index_)
    client_.indices.create(index=index_, mappings=mappings)


def es_insert(client_, index_, id_, doc_):
    resp = client_.index(index=index_, id=id_, document=doc_)
    print("es_insert: ", resp['result'])
    client_.indices.refresh(index=index)


# bulk插入多条数据，性能好于循环单条插入 【推荐】
def es_insert_bulk(client_, index_, docs_):
    bulk_data = []
    # print(docs_)
    for i, row in enumerate(docs_):
        bulk_data.append({
            "_index": index_,
            "_id": i + 1,
            "_source": {
                "num": row["num"],
                "name": row["name"]
            }
        })
    resp = bulk(client_, bulk_data)
    print("es_insert_bulk: ", resp)
    client_.indices.refresh(index=index)


def es_count(client_, index_):
    res = client_.cat.count(index=index_, format="json")
    cnt = res[0]['count']
    print("count: ", cnt)
    return cnt


def es_find_by_id(client, index_, id_):
    resp = client.get(index=index_, id=id_)
    print("es_find: ", resp['_source'])


# match_all 查询所有
def es_search(client, index_, body_={"match_all": {}}):
    print("")
    print("query_body:", body_)
    resp = client.search(index=index_, query=body_)
    # print(resp)
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print(hit["_source"])


def es_delete_by_id(client, index_, id_):
    res_ = client.delete(index=index_, id=id_)
    print(res_['result'])


def es_delete_by_query(client, index_, body_={"query": {"match_all": {}}}):
    del_res = es_client.delete_by_query(index=index_, body=body_)
    print(del_res["deleted"])


def es_update(client, index_, id_, body_, retry_on_conflict=10):
    es_client.update(index=index_,
                     id=id_,
                     body=body_,
                     retry_on_conflict=retry_on_conflict)


def es_push(records, index, es):
    # records is a list of records (dictionaries)
    # index is the name of the index to push to
    # es is the Elasticsearch object to use
    bulk_push = []
    for record in records:
        bulk_push.append({"_index": index, "_type": "record", "_source": record})
    helpers.bulk(es, bulk_push)


if __name__ == '__main__':
    # es_hosts = ["http://elastic:dpjhDNS8MfMj@10.134.220.14:9200"]
    # index = "test_fjp"
    es_hosts = ["http://127.0.0.1:9200"]
    index = "fjp_test_index"
    es_client = es_open(es_hosts)

    # 默认查询，没有任何筛选条件，默认显示前10条数据的所有信息
    res = es_client.search(index='test_1')  # index：选择数据库
    print(res)
    exit(0)
    es_create_index(es_client, index)
    doc = {
        "num": 0,
        "name": "a0"
    }
    docs = [{
        "num": 1,
        "name": "a1"
    }, {
        "num": 2,
        "name": "a2"
    }]
    es_insert(es_client, index, 0, doc)

    es_insert_bulk(es_client, index, docs)
    es_count(es_client, index)

    es_search(es_client, index)
    body = {
        "term": {
            "num": 1
        }
    }
    es_search(es_client, index, body)
    # body = {
    #     "terms": {
    #         "num": [1, 2]
    #     }
    # }
    # es_search(es_client, index, body)
    # match_all/term/terms/
    # range/exists/missing/bool/multi_match
    # regexp/prefix/match_phrase
    es_search(es_client, index, es_enum.TERM)
    es_search(es_client, index, es_enum.TERMS)
    es_search(es_client, index, es_enum.MATCH)
    es_search(es_client, index, es_enum.BOOL_MUST)
    es_search(es_client, index, es_enum.PREFIX)
    es_search(es_client, index, es_enum.WILDCARD)
    es_search(es_client, index, es_enum.FROM_SIZE)
    print("*" * 10)
    es_find_by_id(es_client, index, 1)
    es_delete_by_id(es_client, index, "2")

    query = {
        "query": {
            "match": {
                "name": "a0"
            }
        }
    }
    es_delete_by_query(es_client, index, query)
    # es_update(es_client, id_,"")
    es_close(es_client)
