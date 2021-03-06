from config.myconfig import singleton_cfg
import pymysql
import re


class ScrubDb(object):

    def __init__(self):
        db = singleton_cfg.getScrubDB()
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

    def __del__(self):
        self.connect.close()


class ResultsDb(object):

    def __init__(self):
        db = singleton_cfg.getResultsDB()
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

    def __del__(self):
        self.connect.close()


singleton_ScrubDb = ScrubDb()
singleton_ResultsDb = ResultsDb()

