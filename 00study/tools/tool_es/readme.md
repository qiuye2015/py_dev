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