#!/usr/bin/env python
# coding: utf-8

import json
import logging
import sys
import time
import traceback
import warnings

import elasticsearch
import elasticsearch.helpers
from six import itervalues

INSERT_NORMAL = 0
INSERT_REPLACE = 1
INSERT_IGNORE = 2
import mysql.connector as mysql_connector

INSERT_MODES = {INSERT_IGNORE: 'insert ignore', INSERT_REPLACE: 'replace', INSERT_NORMAL: 'insert'}
ESCAPE = "`%s`"
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt='[%(levelname)s %(asctime)s.%(msecs)03d] [%(process)d:%(threadName)s:%(funcName)s:%(lineno)d] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
LOG.addHandler(handler)


class EsModel(object):
    def __init__(self, hosts, username=None, password=None, timeout=120):
        self.hosts = hosts
        self.username = username
        self.password = password
        if all([username, password]):
            http_auth = (self.username, self.password)
        else:
            http_auth = None
        self._es_client = elasticsearch.Elasticsearch(hosts=self.hosts, http_auth=http_auth, timeout=timeout)

    def get_info(self):
        return self.es.info()

    def analyze(self, query, analyzer='standard'):
        iclient = elasticsearch.client.indices.IndicesClient(self.es)
        return iclient.analyze(body={'text': query, 'analyzer': analyzer})

    def scan(
            self,
            query=None,
            scroll="30m",
            preserve_order=False,
            size=1000,
            request_timeout=None,
            clear_scroll=True,
            scroll_kwargs=None,
            **kwargs
    ):
        """
        Simple abstraction on top of the
        :meth:`~elasticsearch.Elasticsearch.scroll` api - a simple iterator that
        yields all hits as returned by underlining scroll requests.

        By default scan does not return results in any pre-determined order. To
        have a standard order in the returned documents (either by score or
        explicit sort definition) when scrolling, use ``preserve_order=True``. This
        may be an expensive operation and will negate the performance benefits of
        using ``scan``.

        :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use
        :arg query: body for the :meth:`~elasticsearch.Elasticsearch.search` api
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg raise_on_error: raises an exception (``ScanError``) if an error is
            encountered (some shards fail to execute). By default we raise.
        :arg preserve_order: don't set the ``search_type`` to ``scan`` - this will
            cause the scroll to paginate with preserving the order. Note that this
            can be an extremely expensive operation and can easily lead to
            unpredictable results, use with caution.
        :arg size: size (per shard) of the batch send at each iteration.
        :arg request_timeout: explicit timeout for each call to ``scan``
        :arg clear_scroll: explicitly calls delete on the scroll id via the clear
            scroll API at the end of the method on completion or error, defaults
            to true.
        :arg scroll_kwargs: additional kwargs to be passed to
            :meth:`~elasticsearch.Elasticsearch.scroll`

        Any additional keyword arguments will be passed to the initial
        :meth:`~elasticsearch.Elasticsearch.search` call::

            scan(es,
                query={"query": {"match": {"title": "python"}}},
                index="orders-*",
                doc_type="books"
            )

        """
        scroll_kwargs = scroll_kwargs or {}

        if not preserve_order:
            query = query.copy() if query else {}
            query["sort"] = "_doc"

        # initial search
        resp = self.es.search(
            body=query, scroll=scroll, size=size, request_timeout=request_timeout, **kwargs
        )
        scroll_id = resp.get("_scroll_id")

        try:
            if query.get('aggs'):
                for agg_name in query['aggs']:
                    for r in resp['aggregations'][agg_name].get('buckets', {}):
                        yield r
            else:
                while scroll_id and resp["hits"]["hits"]:
                    for hit in resp["hits"]["hits"]:
                        yield hit

                    # check if we have any errors

                    # if (resp["_shards"]["successful"] + resp["_shards"]["skipped"]) < resp["_shards"]["total"]:
                    #     logging.warning(
                    #         "Scroll request has only succeeded on %d (+%d skipped) shards out of %d.",
                    #         resp["_shards"]["successful"],
                    #         resp["_shards"]["skipped"],
                    #         resp["_shards"]["total"],
                    #     )
                    #     if raise_on_error:
                    #         raise Exception(
                    #             scroll_id,
                    #             "Scroll request has only succeeded on %d (+%d skiped) shards out of %d."
                    #             % (resp["_shards"]["successful"], resp["_shards"]["skipped"], resp["_shards"]["total"]),
                    #         )
                    while True:
                        try:
                            resp = self.es.scroll(
                                body={"scroll_id": scroll_id, "scroll": scroll}, **scroll_kwargs
                            )
                            scroll_id = resp.get("_scroll_id")
                            break
                        except ConnectionError:
                            time.sleep(5)

        finally:
            if scroll_id and clear_scroll:
                self.es.clear_scroll(body={"scroll_id": [scroll_id]}, ignore=(404,))

    def select(self, query, index, doc_type="_doc", fields=None, offset=0, limit=0, sort=None, result_format=True):
        offset = offset or 0
        limit = limit or 0
        if not limit:
            for record in elasticsearch.helpers.scan(self.es, index=index, doc_type=doc_type, query=query,
                    _source_include=fields, from_=offset, sort=sort):
                yield record['_source'] if result_format else record
        else:
            for record in self.es.search(index=index, doc_type=doc_type,
                    body=query, _source_include=fields, from_=offset, size=limit,
                    sort=sort
            ).get('hits', {}).get('hits', []):
                yield record['_source'] if result_format else record

    def search(self, query, index, doc_type="_doc", fields=None, offset=0, limit=0, sort=None):
        return self.es.search(index=index, doc_type=doc_type, body=query,
            _source_include=fields, from_=offset, size=limit,
            sort=sort)

    def msearch(self, query, index, doc_type="_doc"):
        body = '{}\n%s' % '\n{}\n'.join([json.dumps(q) for q in query])  # header\n body\n
        return self.es.msearch(index=index, doc_type=doc_type, body=body)['responses']

    def msearch_format(self, query, index, doc_type="_doc"):
        body = '{}\n%s' % '\n{}\n'.join([json.dumps(q) for q in query])  # header\n body\n
        return [r['hits']['hits'][0] for r in self.es.msearch(
            index=index, doc_type=doc_type, body=body)['responses'] if r['hits']['hits']]

    def count(self, index, doc_type="_doc", query=None):
        temp_query = {"query": query.get('query', {})}
        if not temp_query['query']:
            temp_query.pop('query')
        return self.es.count(index=index, doc_type=doc_type,
            body=temp_query).get('count', 0)

    def get(self, es_id, index, doc_type="_doc", fields=None):
        ret = self.es.get(index=index, doc_type=doc_type, id=es_id,
            _source_include=fields, ignore=404)
        return ret.get('_source', None)

    def drop(self, query, index, doc_type="_doc"):
        self.refresh(index)
        for record in elasticsearch.helpers.scan(self.es, index=index, doc_type=doc_type, query=query, _source=False):
            self.es.delete(index=index, doc_type=doc_type, id=record['_id'])

    def refresh(self, index):
        """
        Explicitly refresh one or more index, making all operations
        performed since the last refresh available for search.
        """
        self.es.indices.refresh(index=index)

    def copy(self):
        """
        Explicitly refresh one or more index, making all operations
        performed since the last refresh available for search.
        """
        return self

    @property
    def es(self):
        return self._es_client

    def bulk_write(self, data, batch_size=1000, retry=3):
        total = len(data)
        if retry < 0:
            retry = -retry
        elif retry > 10:
            retry = 10
        succeed = 0

        for _ in range(retry):
            try:
                result = elasticsearch.helpers.bulk(self.es, data, request_timeout=150, chunk_size=batch_size,
                    raise_on_error=False, raise_on_exception=False)
                succeed = result[0]
                if len(result) > 1 and result[1]:
                    logging.error(result)
                if succeed == total:
                    return succeed
            except Exception as e:
                logging.error(e, traceback.format_exc())
        return succeed

    @staticmethod
    def _add_time_range(query, field='created_at', starttime=None, endtime=None):
        if starttime or endtime:
            time_range = {'range': {field: {'format': 'epoch_second'}}}
            if starttime:
                time_range['range'][field]['gte'] = starttime
            if endtime:
                time_range['range'][field]['lte'] = endtime
            query['query']['bool']['filter'].append(time_range)
        return query

    @staticmethod
    def _add_highlight(query):
        query['highlight'] = {
            "number_of_fragments": 0,  # fragment 是指一段连续的文字。返回结果最多可以包含几段不连续的文字。默认是5。
            "fragment_size": 0,  # 一段 fragment 包含多少个字符。默认100。
            "require_field_match": False,
            "pre_tags": "<font color=\"red\">",
            "post_tags": "</font>",
            "encoder": "html",
            "fields": {
                "*": {}
            }
        }
        return query

    @staticmethod
    def _add_aggregations_screen_name(query, offset=0, limit=2147483647):
        """
        "aggregations" : {
            "<aggregation_name>" : { <!--聚合的名字 -->
                "<aggregation_type>" : { <!--聚合的类型 -->
                    <aggregation_body> <!--聚合体：对哪些字段进行聚合 -->
                }
                [,"meta" : {  [<meta_data_body>] } ]? <!--元 -->
                [,"aggregations" : { [<sub_aggregation>]+ } ]? <!--在聚合里面在定义子聚合 -->
            }
            [,"<aggregation_name_2>" : { ... } ]*<!--聚合的名字 -->
        }

        聚合后分页详情见 https://blog.csdn.net/laoyang360/article/details/79112946

        :param query:
        :return:
        """
        query['size'] = 0
        query['from'] = offset
        query['aggs'] = {
            "group_agg": {
                "terms": {
                    "field": "user_screen_name",
                    "size": limit,
                    # 'from': offset,
                    "order": [{"_count": "desc"}],
                    # 广度搜索方式数据量越大，那么默认的使用深度优先的聚合模式生成的总分组数就会非常多，
                    # 但是预估二级的聚合字段分组后的数据量相比总的分组数会小很多所以这种情况下使用广度优先的模式能大大节省内存
                    "collect_mode": "breadth_first",
                },

                "aggs": {
                    "%s_%s" % ('user_screen_name', 'top_hits'): {
                        "top_hits": {
                            "size": 1,
                            "sort": [
                                {
                                    "created_at": {
                                        "order": "desc"
                                    }
                                }
                            ],
                            "_source": {
                                "includes": ['user_screen_name', 'text', 'id', 'retweeted']}}}}}}
        return query

    @staticmethod
    def _replace_highlight(data, keyword='text'):
        if keyword not in data['highlight']:
            return data
        if isinstance(data['highlight'][keyword], list):
            data['_source'][keyword] = ''.join(data['highlight'][keyword])
        else:
            data['_source'][keyword] = data['highlight'][keyword]
        return data


class ClientPyMySQL:
    INSERT_NORMAL = 'insert'
    INSERT_REPLACE = 'replace'
    INSERT_IGNORE = 'insert ignore'
    INSERT_MODES = {INSERT_IGNORE, INSERT_REPLACE, INSERT_NORMAL}
    PLACEHOLDER = '%s'

    def __init__(self, host, port, database,
                 user, passwd):
        """
        SteadyDB
        DBUtils.SteadyDB基于兼容DB-API 2接口的数据库模块创建的普通连接，
        实现了"加强"连接。具体指当数据库连接关闭、丢失或使用频率超出限制时，将自动重新获取连接。

        典型的应用场景如下：在某个维持了某些数据库连接的程序运行时重启了数据库，
        或在某个防火墙隔离的网络中访问远程数据库时重启了防火墙。

        mincached:链接池中空闲链接的初始数量
        maxcached:链接池中空闲链接的最大数量
        maxshared:共享链接的最大数量
        maxconnections:建立链接池的最大数量
        blocking:超过最大链接数量时候的表现，为True等待链接数量降低，为false直接报错处理
        maxusage:单个链接的最大重复使用次数
        """

        import pymysql

        from dbutils.pooled_db import PooledDB
        self.dbc = PooledDB(
            creator=pymysql,
            host=host, user=user,
            passwd=passwd,
            database=database if database else None,
            port=port,
            charset='utf8mb4',
            use_unicode=True,
            autocommit=False,
            mincached=1, maxcached=10,
            maxshared=10, maxconnections=10, blocking=False,
            maxusage=None, setsession=None, reset=True,
            failures=None, ping=1,
            # 流式、字典访问
            cursorclass=pymysql.cursors.SSDictCursor)
        self.__pool = self.dbc
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection()
        self._cursor = self._conn.cursor()

    @property
    def dbcur(self):
        try:
            # if self.dbc.unread_result:
            #     self.dbc.get_rows()
            if not self._cursor:
                self.__get_conn()
            return self._cursor
        except (mysql_connector.OperationalError, mysql_connector.InterfaceError):
            self.__get_conn()
            self._cursor.ping(reconnect=True)
            return self._cursor

    # def begin_transaction(self):
    #     self.dbc.begin()
    #
    # def end_transaction(self):
    #     self.dbc.commit()

    def begin_transaction(self):
        return self.dbcur.execute("BE" + "GIN;")

    def end_transaction(self):
        return self.dbcur.execute("COMMIT;")

    def rollback(self):
        return self.dbcur.execute("rollback;")

    def fetch(self):
        result = self.dbcur.fetchone()
        while result is not None:
            result = self.dbcur.fetchone()

    def _execute(self, sql, values=None, commit=False, **kwargs):
        print(sql)
        try:
            if values:
                self.dbcur.execute(sql, values or [])
            else:
                self.dbcur.execute(sql)
            if commit:
                self.dbcur.execute('COMMIT;')

            def _fetch():
                result = self.dbcur.fetchmany(1000)
                while result:
                    # print(result)
                    for r in result:
                        yield r
                    result = self.dbcur.fetchmany(1000)

            return self.dbcur.lastrowid, _fetch()
        except mysql_connector.DatabaseError as ex:
            if ex.errno == 1205:
                logging.critical(traceback.format_exc())
            else:
                raise

    @staticmethod
    def escape(string):
        return '`%s`' % string

    def save_into_db(self, sql, datas, batch_size=1000):
        for i in range((len(datas) + batch_size - 1) // batch_size):
            self._executemany(sql, datas[i * batch_size:(i + 1) * batch_size])

    def _executemany(self, sql_query, params):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # logging.debug("<sql: %s>" % sql_query)
            self.dbcur.execute("BE" + "GIN;")
            self.dbcur.executemany(sql_query, params)
            self.dbcur.execute("COMMIT;")
            return self.dbcur.fetchall()

    def _get_insert_sql(self, _mode=INSERT_NORMAL, _tablename=None, **values):
        if _mode not in self.INSERT_MODES:
            return None

        tablename = self.escape(_tablename)
        res_values = []
        res_keys = []
        if values:
            for k, v in values.items():
                res_keys.append(k)
                res_values.append(v)
            _keys = ", ".join((self.escape(k) for k in res_keys))
            _values = ", ".join([self.PLACEHOLDER, ] * len(values))
            sql_query = "%s INTO %s (%s) VALUES (%s)" % (_mode, tablename, _keys, _values)
        else:
            sql_query = "%s INTO %s DEFAULT VALUES" % (_mode, tablename)
        logging.debug("<sql: %s>", sql_query)
        return sql_query, res_keys, res_values

    def _insert(self, _mode=INSERT_NORMAL, _tablename=None, **values):
        sql, _, _ = self._get_insert_sql(_mode, _tablename, **values)

        if values:
            self.dbcur = self._execute(sql, list(itervalues(values)))
        else:
            self.dbcur = self._execute(sql)
        return self.dbcur.lastrowid

    def insert_many_with_dict_list(
            self, tablename, data,
            mode='INSERT IGNORE',
            # mode='REPLACE',
            batch_size=5000,
            *args,
            **kwargs
    ):
        if not data:
            return

        tablename = self.escape(tablename)
        values = data[0]
        if values:
            _keys = ", ".join((self.escape(k) for k in values))
            _values = ", ".join([self.PLACEHOLDER, ] * len(values))
            # sql_query = "%s INTO %s (%s) VALUES (%s)" % (mode, tablename, _keys, _values)
            sql_query = "%s INTO %s (%s) VALUES (%s)" % (mode, tablename, _keys, _values)
        else:
            # sql_query = "%s INTO %s DEFAULT VALUES" % (mode, tablename)
            sql_query = "%s INTO %s DEFAULT VALUES" % (mode, tablename)
        # self.logger.debug("<sql: %s>", sql_query)
        # self.logger.debug("%s", tuple(data[0][k] for k in values))

        size = max([1, (len(data) + batch_size - 1) // batch_size])
        for i in range(size):
            # self.logger.info("{} {}/{}".format(mode, batch_size * (i + 1), len(data)))
            self._executemany(sql_query, [list(d[k] for k in values) for d in
                                          data[i * batch_size:(i + 1) * batch_size]])
            # self.begin_transaction()
            # self._executemany(sql_query, [list(d[k] for k in values) for d in data[i * batch_size:(i + 1) * batch_size]])
            # self.end_transaction()
        return len(data)
