from common import common
from config.myconfig import singleton_cfg
from db.db import singleton_ScrubDb


class UrlManager(object):

    def __getUrlByDateAndRaceNo(self, year, month, day, race_num):
        urlList = []
        time_str = common.toDoubleDigitStr(day) + '/' + common.toDoubleDigitStr(month) + '/' + str(year)
        u = singleton_cfg.getBaseUrl() + time_str + '&RaceNo=' + str(race_num) + '&All=0#Race' + str(race_num)
        urlList.append(u)
        return urlList

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

    def __getFromRanceNo(self, str_raceNo):
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

    def __getLoadedUrlList(self, start_year, end_year):
        urlList = []
        for year in range(start_year, end_year + 1):
            tableName = singleton_cfg.getTargetExportTable(year)
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(tableName))
                rows = singleton_ScrubDb.cursor.fetchall()
                singleton_ScrubDb.connect.commit()
                for row in rows:
                    u = singleton_cfg.getBaseUrl() + row['race_date'] + '&RaceNo=' + str(row['race_No']) + '&All=0#Race' + str(row['race_No'])
                    if u not in urlList:
                        urlList.append(u)
            else:
                common.log('table[' + tableName + '] not exist')
        return urlList

    def getUrlList(self):
        # time
        str_from_time, str_to_time = singleton_cfg.getTime()
        start_year, start_month, start_day = self.__getFromTime(str_from_time)
        end_year, end_month, end_day = self.__getToTime(str_to_time)
        # race No
        str_from_raceNo, str_to_raceNo = singleton_cfg.getRaceNo()
        start_raceNo = self.__getFromRanceNo(str_from_raceNo)
        end_raceNo = self.__getToRanceNo(str_to_raceNo)
        # url
        urlList = []
        for y in range(start_year, end_year + 1):
            for m in range(start_month, end_month + 1):
                for d in range(start_day, end_day + 1):
                    for r in range(start_raceNo, end_raceNo + 1):
                        url_list = self.__getUrlByDateAndRaceNo(y, m, d, r)
                        urlList += url_list
        common.log('results url count=' + str(len(urlList)))

        # 剔除已爬取的网址
        needSpiderUrlList = []
        loadedUrlList = self.__getLoadedUrlList(start_year, end_year)
        for u in urlList:
            if u not in loadedUrlList:
                needSpiderUrlList.append(u)
        common.log('need spider results url count=' + str(len(needSpiderUrlList)))
        return needSpiderUrlList


singleton_url = UrlManager()

