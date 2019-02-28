import configparser


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_scrub = {}
        self.__db_results = {}
        self.__target = {}
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

        self.__target['race_date'] = self.cf.get('target', 'race_date')
        self.__target['update_table'] = self.cf.get('target', 'update_table')
        pass

    def getScrubDB(self):
        return self.__db_scrub

    def getResultsDB(self):
        return self.__db_results

    def getRaceDate(self):
        return self.__target['race_date']

    def getUpdateResultsTable(self):
        array = self.__target['update_table'].split(',')
        if len(array) == 2:
            return array[0].strip().replace('date', str(self.__target['race_date']))
        else:
            return None

    def getUpdateScrubTable(self):
        array = self.__target['update_table'].split(',')
        if len(array) == 2:
            return array[1].strip()
        else:
            return None


singleton = MyConfig()