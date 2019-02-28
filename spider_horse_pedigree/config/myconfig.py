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

        self.__target['table'] = self.cf.get('target', 'table')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    # target
    def getTargetTable(self):
        return self.__target['table']


singleton = MyConfig()