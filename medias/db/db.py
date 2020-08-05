from config.myconfig import singleton_cfg
import pymysql
import re


class PKMediaDb(object):

    def __init__(self):
        db = singleton_cfg.getSelfDB()
        self.connect = pymysql.connect(
                        host = db['host'],
                        db = db['db'],
                        user = db['user'],
                        password = db['password'],
                        charset = 'utf8',
                        cursorclass = pymysql.cursors.DictCursor)
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


singleton_PKMediaDb = PKMediaDb()

