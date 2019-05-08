import pymysql
import re


class ScrubDb(object):

    def __init__(self):
        self.connect = pymysql.connect(
                        host='localhost',
                        db='scrub',
                        user='scrub',
                        password='123456',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def table_exists(self, table_name):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = [self.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if table_name in table_list:
            return True
        else:
            return False


singleton_ScrubDb = ScrubDb()


