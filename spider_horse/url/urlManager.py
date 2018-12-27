from config.myconfig import singleton as singleton_cfg
from common import common
from db.db import singleton_ScrubDb
import os
import csv

BASE_HORSE_URL = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseNo='

LOST_FILE_NAME = 'lost_horse_code.csv'


class UrlManager(object):

    # 获取某一天比赛的所有horse_code
    def __getHorseCodeByDate(self, year, month, day):
        tableName = singleton_cfg.getUrlSourceTable(year)
        date = common.toDoubleDigitStr(day) + '/' + common.toDoubleDigitStr(month) + '/' + str(year)
        codeList = []
        if singleton_ScrubDb.table_exists(tableName):
            try:
                singleton_ScrubDb.cursor.execute('select horse_code from {} where race_date=%s'.format(tableName), date)
                list = singleton_ScrubDb.cursor.fetchall()
                for row in list:
                    code = row['horse_code'].strip()
                    if code not in codeList:
                        codeList.append(code)
            except Exception as error:
                common.log('[urlManager]__getHorseCodeByDate:', error)
        else:
            common.log('[urlManager]table[', tableName, '] not exist')

        return codeList

    def __parseTime(self, str_time):
        array = str_time.split('-')
        if len(array) == 3:
            return int(array[0]), int(array[1]), int(array[2])
        else:
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

    def __getLoadedHorseCodeList(self):
        codeList = []
        tableName = singleton_cfg.getTargetHorseTable()
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select code from {}'.format(tableName))
            list = singleton_ScrubDb.cursor.fetchall()
            for row in list:
                code = row['code'].strip()
                if code not in codeList:
                    codeList.append(code)
        return codeList

    def getUrlList(self):
        urlList = []
        # 获取时间段内马匹code
        codeList = []
        str_from_time, str_to_time = singleton_cfg.getTime()
        year_from, month_from, day_from = self.__getFromTime(str_from_time)
        year_to, month_to, day_to = self.__getToTime(str_to_time)
        for year in range(year_from, year_to + 1):
            for month in range(month_from, month_to + 1):
                for day in range(day_from, day_to + 1):
                    list = self.__getHorseCodeByDate(year, month, day)
                    for code in list:
                        if code not in codeList:
                            codeList.append(code)
        common.log('[urlManager]' + str_from_time + '->' + str_to_time + ' horse_code count=' + str(len(codeList)))

        # 剔除已爬取到的马匹code
        loaded_horse_code = self.__getLoadedHorseCodeList()
        for code in codeList:
            if code not in loaded_horse_code:
                u = BASE_HORSE_URL + code
                urlList.append(u)
        return urlList

    def getLostUrlList(self):
        codeList = []
        if os.path.exists('url/' + LOST_FILE_NAME):
            csv_reader = csv.reader(open('url/' + LOST_FILE_NAME))
            for row in csv_reader:
                if row[0] not in codeList:
                    codeList.append(row[0])
        else:
            print('lost file not exist')

        urlList = []
        for code in codeList:
            u = BASE_HORSE_URL + code
            urlList.append(u)
        return urlList


singleton = UrlManager()

