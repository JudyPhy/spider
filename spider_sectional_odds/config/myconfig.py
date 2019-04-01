import configparser
from common import common


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_scrub = {}
        self.__db_results = {}
        self.__spider = {}
        self.__readDBCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_scrub['host'] = self.cf.get('db_scrub', 'host')
        self.__db_scrub['db'] = self.cf.get('db_scrub', 'db')
        self.__db_scrub['user'] = self.cf.get('db_scrub', 'user')
        self.__db_scrub['password'] = self.cf.get('db_scrub', 'password')

        self.__db_results['host'] = self.cf.get('db_results', 'host')
        self.__db_results['db'] = self.cf.get('db_results', 'db')
        self.__db_results['user'] = self.cf.get('db_results', 'user')
        self.__db_results['password'] = self.cf.get('db_results', 'password')

        self.__spider['from_date'] = self.cf.get('spider', 'from_date')
        self.__spider['to_date'] = self.cf.get('spider', 'to_date')
        self.__spider['target_table'] = self.cf.get('spider', 'target_table')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    def getResultsDB(self):
        return self.__db_results

    def getFromDate(self):
        array = self.__spider['from_date'].split('-')
        return array[0].strip() + common.toDoubleDigitStr(array[1].strip()) + common.toDoubleDigitStr(array[2].strip())

    def getToDate(self):
        array = self.__spider['to_date'].split('-')
        return array[0].strip() + common.toDoubleDigitStr(array[1].strip()) + common.toDoubleDigitStr(array[2].strip())

    def getTargetTable(self):
        return self.__spider['target_table'].strip()


singleton_cfg = MyConfig()

