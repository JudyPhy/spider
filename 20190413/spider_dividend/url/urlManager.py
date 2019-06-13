from common import common
from config.myconfig import singleton_cfg
from db.db import singleton_ScrubDb

# {0}:20190505
BASE_URL = 'https://racing.hkjc.com/racing/SystemDataPage/racing/ResultsAll-iframe-SystemDataPage.aspx?match_id={0}&lang=English'

RESULTS_TABLE = 'f_race_results_{0}'


class UrlManager(object):

    def __parseTime(self, str_time):
        array = str_time.split('-')
        if len(array) == 3:
            return int(array[0]), int(array[1]), int(array[2])
        return None, None, None

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

    def __getLoadedRaceDateList(self):
        loaded_race_date_list = []
        tableName = singleton_cfg.getTargetExportTable()
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select race_date from {}'.format(tableName))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                race_date = row['race_date']
                if race_date not in loaded_race_date_list:
                    loaded_race_date_list.append(race_date)
        else:
            print('table[' + tableName + '] not exist')
        return loaded_race_date_list

    def __getResultsDate(self, start_year, start_month, start_day, end_year, end_month, end_day):
        race_date_list = []
        for y in range(start_year, end_year + 1):
            tableName = RESULTS_TABLE.replace('{0}', str(y))
            singleton_ScrubDb.cursor.execute('select race_date from {}'.format(tableName))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                array = row['race_date'].split('/')
                day = array[0]
                month = array[1]
                race_date = str(y) + common.toDoubleDigitStr(month) + common.toDoubleDigitStr(day)
                if y == end_year:
                    if (int(month) <= end_month) and (int(day) <= end_day):
                        if race_date not in race_date_list:
                            race_date_list.append(race_date)
                elif y == start_year:
                    if (int(month) >= start_month) and (int(day) >= start_day):
                        if race_date not in race_date_list:
                            race_date_list.append(race_date)
                else:
                    if race_date not in race_date_list:
                        race_date_list.append(race_date)
        return race_date_list

    def getUrlList(self):
        spiderInfo = singleton_cfg.getSpider()
        start_year, start_month, start_day = self.__getFromTime(spiderInfo['from_time'])
        end_year, end_month, end_day = self.__getToTime(spiderInfo['to_time'])

        race_date_list = self.__getResultsDate(start_year, start_month, start_day, end_year, end_month, end_day)
        print('all url count=', len(race_date_list))

        urlList = []
        loaded_race_date_list = self.__getLoadedRaceDateList()
        for race_date in race_date_list:
            if race_date not in loaded_race_date_list:
                u = BASE_URL.replace('{0}', race_date)
                urlList.append(u)
        print('need spider url count=', len(urlList))
        return urlList


singleton_url = UrlManager()

