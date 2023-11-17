import unittest
from common import DB_CREDENTIALS, break_dataset


class TestMYSQL(unittest.TestCase):
    def setUp(self):
        self.USER = DB_CREDENTIALS['mysql']['user']
        self.PASSWORD = DB_CREDENTIALS['mysql']['password']
        self.HOST = DB_CREDENTIALS['mysql']['host']
        self.PORT = int(DB_CREDENTIALS['mysql']['port'])
        self.DATABASE = 'test_data'
        self.TABLE = 'us_health_insurance'

    def test_mysql_ds(self):
        from mindsdb_datasources import MySqlDS

        LIMIT = 400

        mysql_ds = MySqlDS(
            host=self.HOST,
            user=self.USER,
            password=self.PASSWORD,
            database=self.DATABASE,
            port=self.PORT,
            query=' (SELECT * FROM (SELECT * FROM {table} LIMIT {limit}) as t1) UNION ALL (SELECT * FROM (SELECT * FROM {table} LIMIT {limit}) as t1)'.format(table=self.TABLE, limit=int(LIMIT/2))
        )

        mysql_ds.df = break_dataset(mysql_ds.df)

        assert len(mysql_ds) <= LIMIT

        # Our SQL parsing fails here, test if we're still able to filter via the dataframe fallback
        for val in mysql_ds.filter([['sex', 'like','fem']])['sex']:
            assert val == 'female'

        assert len(mysql_ds.filter([['age', '>', 20]], 12)) == 12
        assert len(mysql_ds.filter([['age', '=', 60]], 1)) == 1
        assert len(mysql_ds.filter([['age', '>', 150]], 11)) == 0
