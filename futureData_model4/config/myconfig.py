import configparser
from common import common


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_source = {}
        self.__db_target = {}
        self.__readDBCfg()

        self.__dragon = {}
        self.__readMiddleDataCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_source['host'] = self.cf.get('db_source', 'host')
        self.__db_source['db'] = self.cf.get('db_source', 'db')
        self.__db_source['user'] = self.cf.get('db_source', 'user')
        self.__db_source['password'] = self.cf.get('db_source', 'password')
        self.__db_source['port'] = self.cf.get('db_source', 'port')

        self.__db_target['host'] = self.cf.get('db_target', 'host')
        self.__db_target['db'] = self.cf.get('db_target', 'db')
        self.__db_target['user'] = self.cf.get('db_target', 'user')
        self.__db_target['password'] = self.cf.get('db_target', 'password')
        self.__db_target['port'] = self.cf.get('db_target', 'port')
        pass

    # middle data
    def __readMiddleDataCfg(self):
        self.cf.read("config/middleData.ini")
        self.__dragon['race_date'] = self.cf.get('dragon', 'race_date')
        self.__dragon['export_table'] = self.cf.get('dragon', 'export_table')
        pass

    # dragon
    def getDragonExportTable(self):
        return self.__dragon['export_table']

    # scrub db
    def getSourceDB(self):
        return self.__db_source;

    # race_date (str)
    def getRaceDate(self):
        array = self.__dragon['race_date'].split('-')
        return array[0] + common.toDoubleDigitStr(array[1]) + common.toDoubleDigitStr(array[2])

    # results db
    def getTargetDB(self):
        return self.__db_target;


singleton_cfg = MyConfig()