import configparser
import datetime


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__sipderInfo = {}
        self.__db_self = {}
        self.__target = {}
        self.__readDBCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_self['host'] = self.cf.get('db_self', 'host')
        self.__db_self['db'] = self.cf.get('db_self', 'db')
        self.__db_self['user'] = self.cf.get('db_self', 'user')
        self.__db_self['password'] = self.cf.get('db_self', 'password')

        self.__sipderInfo['base_url'] = self.cf.get('spiderInfo', "base_url")
        self.__sipderInfo['from_time'] = self.cf.get('spiderInfo', "from_time")
        self.__sipderInfo['to_time'] = self.cf.get('spiderInfo', "to_time")
        self.__sipderInfo['from_race_No'] = self.cf.get('spiderInfo', "from_race_No")
        self.__sipderInfo['to_race_No'] = self.cf.get('spiderInfo', "to_race_No")

        self.__target['export_table'] = self.cf.get('target', 'export_table')
        pass

    def getSelfDB(self):
        return self.__db_self

    def getTime(self):
        return self.__sipderInfo['from_time'], self.__sipderInfo['to_time']

    def getRaceNo(self):
        return self.__sipderInfo['from_race_No'], self.__sipderInfo['to_race_No']

    def getBaseUrl(self):
        return self.__sipderInfo['base_url']

    # export table
    def getTargetExportTable(self, year):
        return self.__target['export_table'].replace('year', str(year))


singleton_cfg = MyConfig()