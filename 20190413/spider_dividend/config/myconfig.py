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

        self.__target['export_table'] = self.cf.get('target', 'export_table')

        self.__sipderInfo['from_time'] = self.cf.get('spider', "from_time")
        self.__sipderInfo['to_time'] = self.cf.get('spider', "to_time")
        self.__sipderInfo['from_race_No'] = self.cf.get('spider', "from_race_No")
        self.__sipderInfo['to_race_No'] = self.cf.get('spider', "to_race_No")
        pass

    def getSelfDB(self):
        return self.__db_self

    def getSpider(self):
        return self.__sipderInfo

    def getTime(self):
        return self.__sipderInfo['from_time'], self.__sipderInfo['to_time']

    def getRaceNo(self):
        return self.__sipderInfo['from_race_No'], self.__sipderInfo['to_race_No']

    def getTargetExportTable(self):
        return self.__target['export_table'].strip()


singleton_cfg = MyConfig()