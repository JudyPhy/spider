import configparser
import datetime


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__sipderInfo = {}
        self.__readSpiderCfg()

        self.__db_scrub = {}
        self.__target = {}
        self.__readDBCfg()
        pass

    def __readSpiderCfg(self):
        self.cf.read("config/spiderCfg.ini")
        self.__sipderInfo['base_url']= self.cf.get('raceCard', "base_url")
        self.__sipderInfo['request_day'] = self.cf.get('raceCard', "request_day")
        self.__sipderInfo['from_race_No'] = self.cf.get('raceCard', "from_race_No")
        self.__sipderInfo['to_race_No'] = self.cf.get('raceCard', "to_race_No")
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_scrub['host'] = self.cf.get('db_scrub', 'host')
        self.__db_scrub['db'] = self.cf.get('db_scrub', 'db')
        self.__db_scrub['user'] = self.cf.get('db_scrub', 'user')
        self.__db_scrub['password'] = self.cf.get('db_scrub', 'password')
        self.__db_scrub['port'] = self.cf.get('db_scrub', 'port')

        self.__target['export_card_table'] = self.cf.get('target', 'export_card_table')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    def getRequestDay(self):
        return self.__sipderInfo['request_day']

    def getRaceNo(self):
        return self.__sipderInfo['from_race_No'], self.__sipderInfo['to_race_No']

    def getBaseUrl(self):
        return self.__sipderInfo['base_url']

    # race-card table
    def getTargetRaceCardTable(self):
        return self.__target['export_card_table']


singleton_cfg = MyConfig()