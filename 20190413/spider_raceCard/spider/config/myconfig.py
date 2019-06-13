import configparser
import datetime


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_scrub = {}
        self.__source = {}
        self.__target = {}
        self.__readDBCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_scrub['host'] = self.cf.get('db_scrub', 'host')
        self.__db_scrub['db'] = self.cf.get('db_scrub', 'db')
        self.__db_scrub['user'] = self.cf.get('db_scrub', 'user')
        self.__db_scrub['password'] = self.cf.get('db_scrub', 'password')
        self.__db_scrub['port'] = self.cf.get('db_scrub', 'port')

        self.__source['from_time'] = self.cf.get('source', 'from_time')
        self.__source['to_time'] = self.cf.get('source', 'to_time')
        self.__source['from_race_No'] = self.cf.get('source', 'from_race_No')
        self.__source['to_race_No'] = self.cf.get('source', 'to_race_No')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    def getSource(self):
        return self.__source


singleton_cfg = MyConfig()