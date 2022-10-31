# from https://blog.51cto.com/u_15077533/4064224
# from https://www.aiuai.cn/aifarm1690.html
# 等于查询:term与terms
TERM = {
    "term": {
        "num": 1
    }
}

TERMS = {
    "terms": {
        "num": [1, 2]
    }
}
# 包含查询:match与multi_match
# 匹配name包含"a1"关键字的数据
MATCH = {
    "match": {
        "name": "a1"
    }
}
# 在name和addr里匹配包含深圳关键字的数据
MULTI_MATCH = {
    "multi_match": {
        "query": "深圳",
        "fields": ["name", "addr"]
    }
}
IDS = {
    "ids": {
        "type": "type_name",
        "values": [0, 1]
    }
}

# 复合查询bool
# bool有3类查询关系，must(都满足),should(其中一个满足),must_not(都不满足)

BOOL_MUST = {
    "bool": {
        "must": [
            {
                "term": {
                    "name": "a0"
                }
            },
            {
                "term": {
                    "num": 0
                }
            }
        ]
    }
}
# 切片式查询: 从第2条数据开始，获取3条数据
FROM_SIZE = {
    # 'match_all': {},
    'from': 2,
    'size': 3
}
# 范围查询:
# 前缀查询:
PREFIX = {
    "prefix": {
        "name": "a"
    }
}
# 通配符查询:
WILDCARD = {
    "wildcard": {
        "name": "a*"
    }
}
# 排序:
