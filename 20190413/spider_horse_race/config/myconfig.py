import configparser


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_scrub = {}
        self.__raceDate = {}
        self.__raceNo = {}
        self.__target = {}
        self.__readDBCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_scrub['host'] = self.cf.get('db_self', 'host')
        self.__db_scrub['db'] = self.cf.get('db_self', 'db')
        self.__db_scrub['user'] = self.cf.get('db_self', 'user')
        self.__db_scrub['password'] = self.cf.get('db_self', 'password')

        self.__raceDate['from'] = self.cf.get('source', 'race_date_from')
        self.__raceDate['to'] = self.cf.get('source', 'race_date_to')

        self.__raceNo['from'] = self.cf.get('source', 'race_no_from')
        self.__raceNo['to'] = self.cf.get('source', 'race_no_to')

        self.__target['table'] = self.cf.get('target', 'table')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    # race_date
    def getRaceDate(self):
        return self.__raceDate

    # race_no
    def getRaceNo(self):
        return self.__raceNo

    # target
    def getTargetTable(self):
        return self.__target['table']


singleton = MyConfig()