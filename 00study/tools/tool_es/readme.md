```bash
# 为 Elasticsearch 创建索引
curl -X PUT "http://localhost:9200/my_index" -H 'Content-Type: application/json' -d '
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "description": { "type": "text" }
    }
  }
}'

curl -H 'Content-Type: application/json' "http://localhost:9200/search" -XPUT  -d '
{
  "mappings": {
    "properties": {
      "searchable": {
        "type": "nested",
        "properties": {
          "title": {
            "type": "text"
          },
          "content": {
            "type": "text"
          }
        }
      },
      "metadata": {
        "type": "nested",
        "properties": {
          "tenant_id": {
            "type": "long"
          },
          "type": {
            "type": "integer"
          },
          "created_at": {
            "type": "date"
          },
          "created_by": {
            "type": "keyword"
          },
          "updated_at": {
            "type": "date"
          },
          "updated_by": {
            "type": "keyword"
          }
        }
      },
      "raw": {
        "type": "nested"
      }
    }
  }
}'
```

# mock 数据
```bash
curl -X PUT "http://localhost:9200/test_fjp_bulk_create?pretty" -H 'Content-Type: application/json' -d '
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text", "analyzer": "ik_smart"
      },
      "price": {
        "type": "double"
      }
    }
  }
}
'

curl -X POST "localhost:9200/test_fjp_bulk_create/_bulk?pretty" -H 'Content-Type: application/json' -d'
{ "create": { } }
{"name": "ES实战","price": 120}
{ "create": { } }
{"name": "ES从入门到精通","price": 60}
{ "create": { } }
{"name": "微服务架构 设计模式","price": 160}
{ "create": { } }
{"name": "架构真经","price": 90}
{ "create": { } }
{"name": "spring boot实战","price": 50}
{ "create": { } }
{"name": "高性能mysql","price": 80}
{ "create": { } }
{"name": "java编程思想","price": 100}
{ "create": { } }
{"name": "java进阶1","price": 10}
{ "create": { } }
{"name": "java进阶2","price": 20}
{ "create": { } }
{"name": "java进阶3","price": 30}
{ "create": { } }
{"name": "java进阶4","price": 40}
{ "create": { } }
{"name": "java进阶5","price": 50}
'

curl -XGET "http://localhost:9200/test_fjp_bulk_create/_search?pretty" -H 'Content-Type: application/json' -d'{  "from": 0,  "size": 2}'
curl -XGET "http://localhost:9200/test_fjp_bulk_create/_search?pretty" -H 'Content-Type: application/json' -d'{  "from": 10000,  "size": 1}'
# ES中不推荐采用（from + size）方式进行深度分页的原因
# 参数index.max_result_window主要用来限制单次查询满足查询条件的结果窗口的大小
curl -XPUT "http://localhost:9200/test_fjp_bulk_create/_settings?pretty" -H 'Content-Type: application/json' -d'{   "index.max_result_window" :"5"}'
curl -XGET "http://localhost:9200/test_fjp_bulk_create/_settings/index.max_result_window?pretty"
```

# culster API
```bash
# 查看集群settings
curl --location --request GET 'http://127.0.0.1:9200/_cluster/settings?pretty'

curl -XPUT "http://localhost:9200/_all/_settings?pretty" -H 'Content-Type: application/json' -d'{   "index.blocks.read_only_allow_delete" : null}'


```