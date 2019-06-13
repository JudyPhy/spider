import configparser


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_scrub = {}
        self.__db_results = {}
        self.__table = {}
        self.__readDBCfg()

        self.__db_other = {}
        self.__readOtherDBCfg()
        pass

    def __readOtherDBCfg(self):
        self.cf.read("config/otherDB.ini")
        self.__db_other['host'] = self.cf.get('db_other', 'host')
        self.__db_other['port'] = self.cf.get('db_other', 'port')
        self.__db_other['db'] = self.cf.get('db_other', 'db')
        self.__db_other['user'] = self.cf.get('db_other', 'user')
        self.__db_other['password'] = self.cf.get('db_other', 'password')
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_scrub['host'] = self.cf.get('db_scrub', 'host')
        self.__db_scrub['port'] = self.cf.get('db_scrub', 'port')
        self.__db_scrub['db'] = self.cf.get('db_scrub', 'db')
        self.__db_scrub['user'] = self.cf.get('db_scrub', 'user')
        self.__db_scrub['password'] = self.cf.get('db_scrub', 'password')

        self.__db_results['host'] = self.cf.get('db_results', 'host')
        self.__db_results['port'] = self.cf.get('db_results', 'port')
        self.__db_results['db'] = self.cf.get('db_results', 'db')
        self.__db_results['user'] = self.cf.get('db_results', 'user')
        self.__db_results['password'] = self.cf.get('db_results', 'password')

        self.__table['result_table'] = self.cf.get('table', 'source_result_table')
        pass

    def getOtherDB(self):
        return self.__db_other

    def getScrubDB(self):
        return self.__db_scrub

    def getResultsDB(self):
        return self.__db_results

    def getRaceResultsTable(self):
        return self.__table['result_table']


singleton_cfg = MyConfig()