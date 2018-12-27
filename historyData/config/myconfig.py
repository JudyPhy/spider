import configparser


class MyConfig(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()

        self.__db_source = {}
        self.__db_target = {}
        self.__readDBCfg()

        self.__combine = {}
        self.__horseStarts = {}
        self.__horseScore = {}
        self.__jockeyScore = {}
        self.__trainerScore = {}
        self.__horseAge = {}
        self.__horseSpeed = {}
        self.__currentRating = {}
        self.__dragon = {}
        self.__readMiddleDataCfg()
        pass

    def __readDBCfg(self):
        self.cf.read("config/db.ini")
        self.__db_source['host'] = self.cf.get('db_source', 'host')
        self.__db_source['db'] = self.cf.get('db_source', 'db')
        self.__db_source['user'] = self.cf.get('db_source', 'user')
        self.__db_source['password'] = self.cf.get('db_source', 'password')
        self.__db_source['port'] = self.cf.get('db_source', 'port')

        self.__db_target['host'] = self.cf.get('db_target', 'host')
        self.__db_target['db'] = self.cf.get('db_target', 'db')
        self.__db_target['user'] = self.cf.get('db_target', 'user')
        self.__db_target['password'] = self.cf.get('db_target', 'password')
        self.__db_target['port'] = self.cf.get('db_target', 'port')
        pass

    # middle data
    def __readMiddleDataCfg(self):
        self.cf.read("config/middleData.ini")
        self.__combine['combine_results_from_time'] = self.cf.get('combine', 'combine_results_from_time')
        self.__combine['combine_results_to_time'] = self.cf.get('combine', 'combine_results_to_time')
        self.__combine['combine_results_export_table'] = self.cf.get('combine', 'combine_results_export_table')

        self.__combine['combine_horse_source_table_list'] = self.cf.get('combine', 'combine_horse_source_table_list')
        self.__combine['combine_horse_export_table'] = self.cf.get('combine', 'combine_horse_export_table')

        self.__currentRating['table_before_list'] = self.cf.get('current_rating', 'table_before_list')

        self.__dragon['export_table'] = self.cf.get('dragon', 'export_table')
        pass

    # combine
    def getCombineResultsExportTable(self):
        return self.__combine['combine_results_export_table']

    def getCombineResultsTime(self):
        return int(self.__combine['combine_results_from_time']), int(self.__combine['combine_results_to_time'])

    def getCombineHorseExportTable(self):
        return self.__combine['combine_horse_export_table']

    def getCombineHorseSourceTableList(self):
        tableList = []
        array = self.__combine['combine_horse_source_table_list'].split(',')
        for table in array:
            tableList.append(table.strip())
        return tableList

    # current rating
    def getCurrentRatingBeforeTableList(self):
        tableList = []
        array = self.__currentRating['table_before_list'].split(',')
        for table in array:
            tableList.append(table.strip())
        return tableList

    # dragon
    def getDragonExportTable(self):
        return self.__dragon['export_table']

    # scrub db
    def getSourceDB(self):
        return self.__db_source;

    # results db
    def getTargetDB(self):
        return self.__db_target;


singleton_cfg = MyConfig()