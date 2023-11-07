# coding: utf-8
import os
import unittest

from peewee import *
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import model_to_dict

from mysql_client import connection_context, new_mysql_client

"""
python3 -m pwiz -e mysql -H 127.0.0.1 -p 33065 -u root -t table_id_increment -P adw_prod  > models.py
"""
db_local = PooledMySQLDatabase(
    "adw_mock",
    timeout=3,
    stale_timeout=300,
    max_connections=10,
    charset="utf8mb4",
    host="127.0.0.1",
    port=33065,
    user="root",
    password="123456",
)


class BaseModelTest(Model):
    class Meta:
        database = db_local


# production/collection/datafiles
class ProductionCollectionDatafiles(BaseModelTest):
    data_ak = CharField(constraints=[SQL("DEFAULT ''")])
    data_bucket = CharField(constraints=[SQL("DEFAULT ''")])
    data_data_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    data_data_value = CharField(constraints=[SQL("DEFAULT ''")])
    data_endpoint = CharField(constraints=[SQL("DEFAULT ''")])
    data_sk = CharField(constraints=[SQL("DEFAULT ''")])
    data_storage_type = CharField(constraints=[SQL("DEFAULT ''")])
    # id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    meta_biz_type = CharField(constraints=[SQL("DEFAULT ''")])
    meta_data_size = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    meta_date = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    meta_device_type = CharField(constraints=[SQL("DEFAULT ''")])
    meta_file_name = CharField(constraints=[SQL("DEFAULT ''")])
    meta_file_path = CharField(constraints=[SQL("DEFAULT ''")])
    meta_file_type = CharField(constraints=[SQL("DEFAULT ''")])
    meta_mission_id = CharField(constraints=[SQL("DEFAULT ''")])
    meta_station_id = CharField(constraints=[SQL("DEFAULT ''")])
    meta_topic = CharField(constraints=[SQL("DEFAULT ''")])
    meta_trigger_time = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    meta_uuid = CharField(constraints=[SQL("DEFAULT ''")])
    meta_vehicle_id = CharField(constraints=[SQL("DEFAULT ''")])
    meta_vehicle_uuid = CharField(constraints=[SQL("DEFAULT ''")])
    partition_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rowkey = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sys_create_time = IntegerField(constraints=[SQL("DEFAULT 0")])
    sys_data_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    sys_data_name = CharField(constraints=[SQL("DEFAULT ''")])
    sys_data_size = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    sys_original_ip = CharField(constraints=[SQL("DEFAULT ''")])
    sys_original_path = CharField(constraints=[SQL("DEFAULT ''")])
    sys_original_type = CharField(constraints=[SQL("DEFAULT ''")])
    sys_update_time = IntegerField(constraints=[SQL("DEFAULT 0")])
    sys_update_user = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "table_102"
        indexes = ((("meta_uuid", "rowkey"), True),)
        primary_key = CompositeKey("meta_uuid", "rowkey")


class TestCDMDatafile(unittest.TestCase):
    def setUp(self):
        os.environ["SERVICE_ENV"] = "dev"
        os.environ["ADW_USER"] = "leo.fu1"
        os.environ["ADW_PWD"] = "BHB83ICUGM"

    def tearDown(self):
        del os.environ["SERVICE_ENV"]
        del os.environ["ADW_USER"]
        del os.environ["ADW_PWD"]

    def test_select_by_rowkey(self):
        # 按照rowkey查询
        query = ProductionCollectionDatafiles.select().where(
            ProductionCollectionDatafiles.rowkey == "dad911463bbf54973da35a505ebea59f"
        )
        for m in query:  # m:ProductionCollectionDatafiles
            print(m.rowkey, model_to_dict(m))

    def test_select(self):
        query = ProductionCollectionDatafiles.select(
            ProductionCollectionDatafiles.rowkey,
            ProductionCollectionDatafiles.data_data_value,
            ProductionCollectionDatafiles.data_bucket,
        ).where(
            (ProductionCollectionDatafiles.meta_vehicle_id == "938bf28a32f041e42294739140001110")
            & (ProductionCollectionDatafiles.meta_file_type == "json")
        )
        for m in query:
            # print(m.rowkey, model_to_dict(m))
            rowkey = m.rowkey
            bucket = m.data_bucket
            key = m.data_data_value
            print(f"rowkey={rowkey}, bucket={bucket}, key={key}")


class BaseModel(Model):
    class Meta:
        database = new_mysql_client()


class Datafiles(BaseModel):
    data_bucket = CharField(constraints=[SQL("DEFAULT ''")])
    data_data_value = CharField(constraints=[SQL("DEFAULT ''")])
    meta_file_path = CharField(constraints=[SQL("DEFAULT ''")])
    meta_task_id = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    partition_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    rowkey = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    sys_create_time = IntegerField(constraints=[SQL("DEFAULT 0")])
    sys_update_time = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'table_38'
        indexes = ((('meta_car_id',), False),)


class TestDatafile(unittest.TestCase):
    def setUp(self):
        os.environ["SERVICE_ENV"] = "dev"
        os.environ["ADW_USER"] = "leo.fu1"
        os.environ["ADW_PWD"] = "BHB83ICUGM"

    def tearDown(self):
        del os.environ["SERVICE_ENV"]
        del os.environ["ADW_USER"]
        del os.environ["ADW_PWD"]

    def iter(self, filters=[], limit=100, total=None, order_bys=None, columns=None):
        """分页迭代器"""
        offset = 0
        while True:
            with connection_context(new_mysql_client()):
                result = (
                    Datafiles.select(columns).where(*filters).order_by(*order_bys).limit(limit).offset(offset).execute()
                )

            cnt = 0
            for e in result:
                cnt += 1
                yield e

            if cnt < limit:
                break
            offset += limit
            if total is not None and offset >= total:
                break

    def get_bucket_key(self, task_id, file_path=None):
        filters = [
            Datafiles.meta_task_id == task_id,
            Datafiles.meta_file_path.startswith(file_path) if file_path else None,
        ]
        self.iter(
            filters=filters,
            limit=100,
            total=None,
            order_bys=[Datafiles.rowkey.asc()],
            columns=[Datafiles.data_bucket, Datafiles.data_data_value, ProductionCollectionDatafiles.rowkey],
        )

    def test_select(self):
        query = ProductionCollectionDatafiles.select(
            ProductionCollectionDatafiles.rowkey,
            ProductionCollectionDatafiles.data_data_value,
            ProductionCollectionDatafiles.data_bucket,
        ).where(
            (ProductionCollectionDatafiles.meta_vehicle_id == "938bf28a32f041e42294739140001110")
            & (ProductionCollectionDatafiles.meta_file_type == "json")
        )
        for m in query:
            # print(m.rowkey, model_to_dict(m))
            rowkey = m.rowkey
            bucket = m.data_bucket
            key = m.data_data_value
            print(f"rowkey={rowkey}, bucket={bucket}, key={key}")


class TestBaseDemo(unittest.TestCase):
    def test_connect(self):
        from playhouse.db_url import connect

        mysql_config_url = "mysql+pool://root:123456@127.0.0.1:33065/appmanage?max_connections=300&stale_timeout=300"
        db = connect(url=mysql_config_url)

    def test_conn_pool(self):
        from playhouse.db_url import connect

        mysql_config_url = "mysql+pool://root:123456@127.0.0.1:33065/appmanage?max_connections=300&stale_timeout=300"
        db = connect(url=mysql_config_url)
        with db.connection_context():
            pass
            # A new connection will be opened or, if using a connection pool,
            # pulled from the pool of available connections. Additionally, a
            # transaction will be started.
