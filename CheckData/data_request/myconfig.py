import configparser


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_results = {}
        self.__table = {}
        self.__readDBCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("../data_request/db.ini")
        self.__db_results['host'] = self.cf.get('db_results', 'host')
        self.__db_results['port'] = self.cf.get('db_results', 'port')
        self.__db_results['db'] = self.cf.get('db_results', 'db')
        self.__db_results['user'] = self.cf.get('db_results', 'user')
        self.__db_results['password'] = self.cf.get('db_results', 'password')

        self.__table['result_table'] = self.cf.get('table', 'source_table')
        pass

    def getResultsDB(self):
        return self.__db_results

    def getResultsTable(self):
        return self.__table['result_table']


singleton = MyConfig()