import configparser
import datetime


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__sipderInfo = {}
        self.__db_self = {}
        self.__readDBCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_self['host'] = self.cf.get('db_self', 'host')
        self.__db_self['db'] = self.cf.get('db_self', 'db')
        self.__db_self['user'] = self.cf.get('db_self', 'user')
        self.__db_self['password'] = self.cf.get('db_self', 'password')
        pass

    def getSelfDB(self):
        return self.__db_self


singleton_cfg = MyConfig()