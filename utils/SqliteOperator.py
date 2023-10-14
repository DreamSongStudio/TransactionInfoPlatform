import sqlite3


class SqliteOperator:
    def __init__(self, sql_name='memory'):
        self.con = sqlite3.connect(sql_name)
        self.cur = self.con.cursor()

    def execute(self, sql):
        self.cur.execute(sql)
        self.con.commit()

    def executemany(self, sql, params):
        self.cur.executemany(sql, params)
        self.con.commit()

    def insert(self, sql):
        self.execute(sql)

    def query(self, sql, ret_type='all'):
        """
        type=all时全量查询，返回对象数组
        type=one时，只查询一个，返回单个对象
        :param sql:
        :param ret_type: all
        :return:
        """
        self.cur.execute(sql)
        desc = self.cur.description

        if ret_type == 'all':
            data = self.cur.fetchall()
            return [dict(zip([col[0] for col in desc], row)) for row in data]
        elif ret_type == 'one':
            if self.cur.rowcount > 0:
                data = self.cur.fetchone()
                return dict(zip([col[0] for col in desc], data))
            else:
                return {}
        elif ret_type == 'count':
            return self.cur.rowcount
        elif ret_type == 'aggregation':
            return self.cur.fetchall()


# if __name__ == '__main__':
#     test = SqliteOperator('test')
#     test.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY,name TEXT,age INTEGER)")
    # data = "1,'leon',22"
    # test.execute(f'INSERT INTO test VALUES ({data})')
    # 批量插入
    # data = [(2,'asd',223), (3,'xxxx',54), (4,'ddddd',32),  (5,'ggggg',3), ]
    # test.executemany(f'INSERT INTO test VALUES (?,?,?)', data)
    # # 查询数据
    # print(test.query('select * from test order by id desc', 'one'))


