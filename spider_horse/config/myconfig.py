import configparser


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
        self.__db_scrub['host'] = self.cf.get('db_self', 'host')
        self.__db_scrub['db'] = self.cf.get('db_self', 'db')
        self.__db_scrub['user'] = self.cf.get('db_self', 'user')
        self.__db_scrub['password'] = self.cf.get('db_self', 'password')

        self.__source['lost_horse'] = self.cf.get('time', 'lost_horse')
        self.__source['time_from'] = self.cf.get('time', 'from')
        self.__source['time_to'] = self.cf.get('time', 'to')
        self.__source['results_table'] = self.cf.get('source', 'results_table')

        self.__target['table'] = self.cf.get('target', 'table')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    # lost horse
    def spiderLost(self):
        return self.__source['lost_horse'] == '1'

    # time range
    def getTime(self):
        return self.__source['time_from'], self.__source['time_to']

    # source
    def getUrlSourceTable(self, year):
        tableName = self.__source['results_table'].replace('year', str(year))
        return tableName

    # target
    def getTargetHorseTable(self):
        return self.__target['table']


singleton = MyConfig()