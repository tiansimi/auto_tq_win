# -*- coding:utf-8 -*-
# @Time   : 2021/11/29 15:19
# @Author : tq
# @File   : sqlite.py
import os
import sqlite3

from conf.confpath import ConfPath
from conf.config import conf
from common.log import log


class Sqlite:
    def __init__(self, db):
        self.db = db
        self._conn, self._curs = self._get_conn_curs()

    def close(self):
        """ 关闭游标和连接 """
        try:
            if self._curs:
                self._curs.close()
        except Exception as e:
            log.error(e)
            raise e
        finally:
            if self._conn:
                self._conn.close()

    def _get_conn(self):
        """ 获取连接 """
        conn = sqlite3.connect(self.db)
        return conn

    def _get_cursor(self, conn):
        """ 获取游标 """
        return conn.cursor()

    def _get_conn_curs(self):
        """ 获取连接和游标 """
        conn = self._get_conn()
        curs = self._get_cursor(conn)
        return conn, curs

    def select(self, select_sql):
        """
        查询 sql 语句，返回所有数据
        :param select_sql: 查询 sql 语句
        :return: [(20,1,55),(24,2,53),(25,1,57)]
        """
        try:
            self._curs.execute(select_sql)
        except sqlite3.Error as e:
            log.error(f'SQL有误!\nselect语句：{select_sql}\n错误内容: {e}')
            raise
        else:
            if self._curs.rowcount == 1:
                result = self._curs.fetchone()
                log.info(f'select执行成功!\nselect语句:"{select_sql}"\n结果 1 条数据')
                self.close()
                log.info(f'数据记录1为：{result}')
                return result
            else:
                result = self._curs.fetchall()
                log.info(f'select执行成功!select_all语句:"{select_sql}"结果 {len(result)} 条数据')
                self.close()
                log.info(f'数据记录all为：{result}')
                return result

    def update_delete_insert(self, sql):
        """
        执行 更新、删除、插入操作
        :param sql: sql 语句
        :return:
        """
        try:
            self._curs.execute(sql)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            log.error(f'sql 执行失败,已进行回滚操作!\nsql 语句:"{sql}"\n失败内容为:{e}')
            raise
        else:
            # 判断是否更新成功
            if self._curs.rowcount == 1:
                log.info(f'sql 执行成功!\nsql语句:"{sql}"')
            else:
                log.warning(f'sql 执行成功!\nsql语句:"{sql}"\nwarning:更新后的值与跟新之前的值相等，或者查询不到对应的结果')
        finally:
            self.close()
            return self._curs.rowcount

    def select_field(self, select_sql):
        """
        查询数据: 带字段名称和数据
        :param select_sql: 查询语句
        :return: ((字段名称1,字段名称2),[(第1行值1，第1行值2),(第2行值1，第2行值2)])
        """
        try:
            self._curs.execute(select_sql)
            field = [f[0] for f in self._curs.description]
        except Exception as e:
            log.error(f'SQL有误!\nselect语句:"{select_sql}"\n错误内容 {e}')
            raise
        else:
            if self._curs.rowcount == 1:
                result = field, list(self._curs.fetchone())
                log.info(f'select执行成功!\nselect语句:"{select_sql}"\n结果 1 条数据')
                log.info(f'数据记录为：{result}')
                self.close()
                return result
            else:
                result = field, list(self._curs.fetchall())
                log.info(f'select执行成功!\nselect语句:"{select_sql}"\n结果 n 条数据')
                self.close()
                log.info(f'数据记录为：{result}')
                return result


if __name__ == '__main__':
    db = os.path.join(ConfPath.DB_DIR, conf.db_log_file)
    s = Sqlite(db)
    sql = r"select count(*) from HrLogV3;"
    # sql = r'select detail from HrLogV3 order by ts desc limit 1;'
    data = s.select(sql)



