from common import common
from config.myconfig import singleton_cfg
from db.db import singleton_ScrubDb

# BASE_URL = 'https://racing.hkjc.com/racing/Info/Meeting/Results/English/Local'
BASE_URL = 'https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate={0}&Racecourse={1}&RaceNo={2}'    #{0}:2019/03/13  {1}:HV  {2}:1

RACE_TYPE = ['ST', 'HV']


class UrlManager(object):

    def __getUrlByDateAndRaceNo(self, year, month, day, race_num):
        urlList = []
        time_str = str(year) + common.toDoubleDigitStr(month) + common.toDoubleDigitStr(day)
        for type in RACE_TYPE:
            # u = BASE_URL + '/' + time_str + '/' + type + '/' + str(race_num)
            u = BASE_URL.replace('{0}', str(year) + '/' + common.toDoubleDigitStr(month) + '/' + common.toDoubleDigitStr(day)).replace('{1}', type).replace('{2}', str(race_num))
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
            tableName = singleton_cfg.getTargetRaceResultsTable(year)
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(tableName))
                list = singleton_ScrubDb.cursor.fetchall()
                singleton_ScrubDb.connect.commit()
                for row in list:
                    array = row['race_date'].split('/')
                    if len(array) == 3:
                        str_url_date = array[2] + array[1] + array[0]
                        for type in RACE_TYPE:
                            # u = BASE_URL + '/' + str_url_date + '/' + type + '/' + str(row['race_No'])
                            u = BASE_URL.replace('{0}', array[2] + '/' + array[1] + '/' + array[0]).replace('{1}', type).replace('{2}', str(row['race_No']))
                            if u not in urlList:
                                urlList.append(u)
                    else:
                        common.log('race_date[' + row['race_date'] + ' error')
            else:
                common.log('table[' + tableName + '] not exist')
        return urlList

    def getUrlList(self):
        spiderInfo = singleton_cfg.getSpider()
        # time
        # str_from_time, str_to_time = singleton_cfg.getTime()
        start_year, start_month, start_day = self.__getFromTime(spiderInfo['from_time'])
        end_year, end_month, end_day = self.__getToTime(spiderInfo['to_time'])
        # race No
        # str_from_raceNo, str_to_raceNo = singleton_cfg.getRaceNo()
        start_raceNo = self.__getFromRanceNo(spiderInfo['from_race_No'])
        end_raceNo = self.__getToRanceNo(spiderInfo['to_race_No'])
        # url
        urlList = []
        for y in range(start_year, end_year + 1):
            for m in range(start_month, end_month + 1):
                for d in range(start_day, end_day + 1):
                    for r in range(start_raceNo, end_raceNo + 1):
                        list = self.__getUrlByDateAndRaceNo(y, m, d, r)
                        urlList += list
        common.log('results url count=' + str(len(urlList)))

        # 剔除已爬取的网址
        needSpiderUrlList = []
        loadedUrlList = self.__getLoadedUrlList(start_year, end_year)
        for u in urlList:
            if u not in loadedUrlList:
                needSpiderUrlList.append(u)
        common.log('need spider results url count=' + str(len(needSpiderUrlList)))
        return needSpiderUrlList


singleton = UrlManager()

