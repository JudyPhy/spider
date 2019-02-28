from config.myconfig import singleton_cfg
import pymysql
import re


class ScrubDB(object):

    def __init__(self):
        db = singleton_cfg.getSourceDB()
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


class ResultsDB(object):

    def __init__(self):
        db = singleton_cfg.getTargetDB()
        self.connect = pymysql.connect(
            host=db['host'],
            db=db['db'],
            user=db['user'],
            password=db['password'],
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


class CustomDatabase(object):

    def __init__(self, theHost, thePort, theDb, therUer, thePassword):
        db = singleton_cfg.getTargetDB()
        self.connect = pymysql.connect(
            host=theHost,
            port=thePort,
            db=theDb,
            user=therUer,
            password=thePassword,
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


singleton_Scrub_DB = ScrubDB()
singleton_Results_DB = ResultsDB()

