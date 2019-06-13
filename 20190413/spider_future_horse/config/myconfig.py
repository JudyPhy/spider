import configparser
from common import common


class MyConfig(object):

    RACE_CARD_TABLE = 't_race_card_future_{0}'

    TARGET_TABLE = 'a_future_horse_info_{0}'

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_scrub = {}
        self.__source = {}
        self.__target = {}
        self.__readDBCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_scrub['host'] = self.cf.get('db_self', 'host')
        self.__db_scrub['db'] = self.cf.get('db_self', 'db')
        self.__db_scrub['user'] = self.cf.get('db_self', 'user')
        self.__db_scrub['password'] = self.cf.get('db_self', 'password')

        self.__source['race_date'] = self.cf.get('source', 'race_date')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    # source
    def getRaceDate(self):
        array = self.__source['race_date'].strip().split('-')
        return array[0] + common.toDoubleDigitStr(array[1]) + common.toDoubleDigitStr(array[2])

    def getRaceCardTable(self):
        return self.RACE_CARD_TABLE

    def getTargetTable(self):
        return self.TARGET_TABLE


singleton_cfg = MyConfig()

