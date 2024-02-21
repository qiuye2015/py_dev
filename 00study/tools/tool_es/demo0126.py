import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def update_doc(hit):
    doc = hit["_source"]
    tag = json.loads(doc.get('tag')[0][len('attr`'):])
    admin_code = tag.get('features', {}).get('admin_code', '')
    if len(admin_code) >= 4:
        doc["lbs_location"] = {
            "city_code": admin_code[:4],
            "pro_code": admin_code[:2]
        }
        print(f"update {hit['_id']}")
        return {
            "_op_type": "update",
            "_index": hit["_index"],
            "_id": hit["_id"],
            "doc": doc
        }
    else:
        print(f"filter {hit['_id']}")


def get_docs(es, index, query, scroll_time):
    result = es.search(index=index, body=query, scroll=scroll_time)
    while result["hits"]["hits"]:
        for hit in result["hits"]["hits"]:
            r = update_doc(hit)
            if r is not None:
                yield r
        result = es.scroll(scroll_id=result["_scroll_id"], scroll=scroll_time)


es = Elasticsearch("http://localhost:9200")
my_index = 'fjp_dlb_geofence_v1'
batch_size = 2
scroll_time = "5m"
# query = {"query": {"term": {"artifact_name": "mapstub_polyline_0908_suzhou"}}, "size": batch_size}
query = {"query": {"match_all": {}}, "size": batch_size}
docs = get_docs(es, my_index, query, scroll_time)

# Assuming docs is your list of actions
success, failed_or_errors = bulk(es, docs, stats_only=False)

# Check for errors
if isinstance(failed_or_errors, list) and len(failed_or_errors) > 0:
    print("Some documents could not be updated, success count: {success}")
    for item in failed_or_errors:
        print(f"Error updating document {item['update']['_id']}: {item['update']['error']}")
elif isinstance(failed_or_errors, int) and failed_or_errors > 0:
    print(f"{failed_or_errors} documents failed to update, success count: {success}")
else:
    print(f"All documents updated successfully. {success}, failed={failed_or_errors}")


def demo():
    import json

    from elasticsearch import Elasticsearch

    # 创建 Elasticsearch 客户端实例
    es = Elasticsearch("http://localhost:9200")
    my_index = 'fjp_dlb_geofence_v1'
    batch_size = 2
    scroll_time = "1m"
    # 定义查询语句，使用 Scroll API 获取所有数据
    # query = {"query": {"match_all": {}}, "size": batch_size}
    query = {"query": {
        "term": {
            "artifact_name": "mapstub_polyline_0908_suzhou"
        }
    }, "size": batch_size}

    result = es.search(index=my_index, body=query, scroll=scroll_time)

    # 获取第一批数据和 scroll_id
    scroll_id = result["_scroll_id"]
    hits = result["hits"]["hits"]

    # 定义 Bulk API 请求体
    bulk_body = ""
    for hit in hits:
        # 修改数据，添加新字段
        doc = hit["_source"]
        tag = json.loads(doc.get('tag')[0][len('attr`'):])
        admin_code = tag.get('features', {}).get('admin_code', '')
        if len(admin_code) >= 4:
            doc["lbs_location"] = {
                "city_code": admin_code[:4],
                "pro_code": admin_code[:2]
            }
            print(f"update {hit['_id']}")
        else:
            print(f"filter {hit['_id']}")
            continue

        # 定义 Bulk API 请求体
        bulk_body += json.dumps({"update": {"_id": hit["_id"], "_index": hit["_index"]}}) + "\n"
        bulk_body += json.dumps({"doc": doc}) + "\n"

    # 使用 Bulk API 批量插入数据
    while len(hits) > 0:
        # 执行 Bulk API 请求
        r = es.bulk(index=my_index, body=bulk_body)
        print(f"es bulk {my_index},bulk_body={bulk_body},{json.dumps(r)}")

        # 使用 Scroll API 获取下一批数据
        result = es.scroll(scroll_id=scroll_id, scroll=scroll_time)
        scroll_id = result["_scroll_id"]
        hits = result["hits"]["hits"]

        # 生成 Bulk API 请求体
        bulk_body = ""
        for hit in hits:
            # 修改数据，添加新字段
            doc = hit["_source"]
            doc["new_field"] = "new_value"

            # 定义 Bulk API 请求体
            bulk_body += json.dumps({"update": {"_id": hit["_id"], "_index": hit["_index"]}}) + "\n"
            bulk_body += json.dumps({"doc": doc}) + "\n"
