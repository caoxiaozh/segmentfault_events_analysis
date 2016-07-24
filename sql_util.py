# coding:utf8
import pymysql.cursors


class SqlUtil(object):

    @staticmethod
    def get_connection():
        connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='blog',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        return connection

    @staticmethod
    def query_all(sql):
        connection = SqlUtil.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
