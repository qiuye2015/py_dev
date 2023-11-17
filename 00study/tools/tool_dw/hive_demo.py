from loguru import logger


class Presto:
    try:
        from pyhive import presto
    except Exception as err_msg:
        print(err_msg)

    def __init__(self, config):
        self.__config = config

    def _presto_connect(self, host, port, username):
        return self.presto.connect(host=host, port=port, username=username)

    def _get_cursor(self):
        try:
            cursor = self._presto_connect(
                host=self.__config['host'],
                port=self.__config['port'],
                username=self.__config['user']).cursor()
        except Exception as e:
            logger.exception(f'presto connection failure: {e}')
        return cursor

    def prestoTableColumns(self, table):
        cursor = self._get_cursor()
        try:
            sql_stmt = '''select * from {} where 1=2 '''.format(table)
            cursor.execute(sql_stmt)
            columns_list = [t[0] for t in cursor.description]
            return columns_list
        except Exception as e:
            logger.exception(f'presto select failure: {e}')
        finally:
            cursor.close()

    def prestoTableColumnsType(self, table):
        cursor = self._get_cursor()
        try:
            sql_stmt = '''select * from {} where 1=2 '''.format(table)
            cursor.execute(sql_stmt)
            column_type = {}
            for col in cursor.description:
                column_type[col[0]] = col[1]
            return column_type
        except Exception as e:
            logger.exception(f'presto select failure: {e}')
        finally:
            cursor.close()

    def prestoSelect(self, sql, withcolumns=None):
        cursor = self._get_cursor()
        try:
            cursor.execute(sql)
            data_cursor = cursor.fetchall()
            # 如果没有输入列，则返回列表元组
            if withcolumns is None:
                return data_cursor

            data_list = []
            # 如果输入列名，则返回列表字典
            # tuple to dict
            columns_list = [t[0] for t in cursor.description]
            for row in data_cursor:
                row_dict = {}
                for i in range(len(columns_list)):
                    row_dict[columns_list[i]] = row[i]
                data_list.append(row_dict)
            return data_list
        except Exception as err_msg:
            logger.error(f"{err_msg}")
            return None
        finally:
            if cursor is not None:
                cursor.close()


def main():
    _presto = Presto(config={
        "host": "127.0.0.1",
        "port": 9000,
        "user": "hadoop01",
    })
    # print(_presto.prestoSelect('select 1'))
    # print(_presto.prestoTableColumns("orders"))
    # print(_presto.prestoTableColumnsType("orders"))

if __name__ == '__main__':
    main()
