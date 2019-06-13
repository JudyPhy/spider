from ..common import common
from ..config.myconfig import singleton_cfg
from ..db.db import singleton_ScrubDb

RACE_TYPE = ['ST', 'HV']

BASE_URL = 'https://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/{0}/{1}/{2}'    # 20190224, ST/HV, raceNo

RESULTS_TABLE = 'f_race_results_YEAR'


class UrlManager(object):

    isHistory = False

    def __getLoadedParam(self, tableNameList):
        date_No_dic = {}  # race_date & [raceNo]
        for tableName in tableNameList:
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(tableName)) # race_data: 20190101
                rows = singleton_ScrubDb.cursor.fetchall()
                singleton_ScrubDb.connect.commit()
                for row in rows:
                    race_date = row['race_date']
                    if race_date not in date_No_dic.keys():
                        date_No_dic[race_date] = []
                    race_No = row['race_No']
                    if race_No not in date_No_dic[race_date]:
                        date_No_dic[race_date].append(race_No)
        return date_No_dic

    def __parseTime(self, str_time):
        array = str_time.split('-')
        if len(array) == 3:
            return int(array[0]), int(array[1]), int(array[2])
        return 0, 0, 0

    def __getFromTime(self, str_time):
        year, month, day = self.__parseTime(str_time)
        if year != 0:
            if month != 0:
                if day != 0:
                    return year, month, day
                else:
                    return year, month, 1
            else:
                if day != 0:
                    return year, 1, day
                else:
                    return year, 1, 1
        else:
            return None, None, None

    def __getToTime(self, str_time):
        year, month, day = self.__parseTime(str_time)
        if year != 0:
            if month != 0:
                if day != 0:
                    return year, month, day
                else:
                    return year, month, 31
            else:
                if day != 0:
                    return year, 12, day
                else:
                    return year, 12, 31
        else:
            return None, None, None

    def __getFromRaceNo(self, str_raceNo):
        no = int(str_raceNo)
        if no != 0:
            return no
        else:
            return 1

    def __getToRanceNo(self, str_raceNo):
        no = int(str_raceNo)
        if no != 0:
            return no
        else:
            return 11

    def getHistoryUrlList(self):
        self.isHistory = True
        # time
        source = singleton_cfg.getSource()
        from_year, from_month, from_day = self.__getFromTime(source['from_time'])
        to_year, to_month, to_day = self.__getToTime(source['to_time'])
        start_raceNo = self.__getFromRaceNo(source['from_race_No'])
        end_raceNo = self.__getToRanceNo(source['to_race_No'])
        # get useful date and raceNo
        date_No_dic = {}    # race_date & [raceNo]
        for year in range(from_year, to_year + 1):
            tableName = RESULTS_TABLE.replace('YEAR', str(year))
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(tableName))
                rows = singleton_ScrubDb.cursor.fetchall()
                singleton_ScrubDb.connect.commit()
                for row in rows:
                    array_date = row['race_date'].split('/')
                    month = int(array_date[1])
                    day = int(array_date[0])
                    race_No = row['race_No']
                    if (month >= from_month) and (month <= to_month) \
                            and (day >= from_day) and (day <= to_day) \
                            and (race_No >= start_raceNo) and (race_No <= end_raceNo):
                        race_date = array_date[2] + array_date[1] + array_date[0]
                        if race_date not in date_No_dic.keys():
                            date_No_dic[race_date] = []
                        if race_No not in date_No_dic[race_date]:
                            date_No_dic[race_date].append(race_No)
        n = 0
        for race_date, raceNoList in date_No_dic.items():
            n += len(raceNoList)
        print('all count:', n)

        tableNameList = []
        for year in range(from_year, to_year + 1):
            tableNameList.append('t_race_card_' + str(year))
        loaded_dict = self.__getLoadedParam(tableNameList)
        m = 0
        for race_date, raceNoList in date_No_dic.items():
            m += len(raceNoList)
        print('loaded count:', m)

        urlList = []
        for race_date, raceNoList in date_No_dic.items():
            for race_no in raceNoList:
                if (race_date in loaded_dict.keys()) and (race_no in loaded_dict[race_date]):
                    continue
                for type in RACE_TYPE:
                    u = BASE_URL.replace('{0}', race_date).replace('{1}', type).replace('{2}', str(race_no))
                    urlList.append(u)
        # u = BASE_URL.replace('{0}', '20190505').replace('{1}', 'ST').replace('{2}', str(4))
        # urlList.append(u)
        return urlList

    def getFutureUrlList(self):
        self.isHistory = False
        urlList = []
        # time
        source = singleton_cfg.getSource()
        from_year, from_month, from_day = self.__getFromTime(source['from_time'])
        to_year, to_month, to_day = self.__getToTime(source['to_time'])
        start_raceNo = self.__getFromRaceNo(source['from_race_No'])
        end_raceNo = self.__getToRanceNo(source['to_race_No'])
        for year in range(from_year, to_year + 1):
            for month in range(from_month, to_month + 1):
                for day in range(from_day, to_day + 1):
                    for race_no in range(start_raceNo, end_raceNo + 1):
                        for type in RACE_TYPE:
                            race_date = str(year) + common.toDoubleDigitStr(month) + common.toDoubleDigitStr(day)
                            u = BASE_URL.replace('{0}', race_date).replace('{1}', type).replace('{2}', str(race_no))
                            urlList.append(u)
        return urlList


singleton_url = UrlManager()

