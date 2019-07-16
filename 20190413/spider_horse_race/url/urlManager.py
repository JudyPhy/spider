from config.myconfig import singleton as singleton_cfg
from common import common
from db.db import singleton_ScrubDb

# BASE_HORSE_URL = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseNo='
HORSE_URL_PRE = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseNo='
HORSE_URL_EX = '&Option=1'

RESULTS_TABLE = 'f_race_results_YEAR'

class UrlManager(object):

    def __getLoadedHorseCodeList(self):
        codeList = []
        tableName = singleton_cfg.getTargetTable()
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select code from {}'.format(tableName))
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            code = row['code'].strip()
            if code not in codeList:
                codeList.append(code)
        return codeList


    def __parseDate(self, date):
        array = date.split('-')
        return int(array[0]), int(array[1]), int(array[2])

    def __getFromDate(self, date):
        year, month, day = self.__parseDate(date)
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

    def __getToDate(self, date):
        year, month, day = self.__parseDate(date)
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

    def __getToRaceNo(self, str_raceNo):
        no = int(str_raceNo)
        if no != 0:
            return no
        else:
            return 11

    def getUrlList(self):
        raceDate = singleton_cfg.getRaceDate()
        from_y, from_m, from_d = self.__getFromDate(raceDate['from'])
        to_y, to_m, to_d = self.__getToDate(raceDate['to'])
        raceNo = singleton_cfg.getRaceNo()
        from_no = self.__getFromRaceNo(raceNo['from'])
        to_no = self.__getToRaceNo(raceNo['to'])

        horseCodeList = []
        for y in range(from_y, to_y + 1):
            tableName = RESULTS_TABLE.replace('YEAR', str(y))
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute('select race_date,horse_code,race_No from {}'.format(tableName))
                rows = singleton_ScrubDb.cursor.fetchall()
                singleton_ScrubDb.connect.commit()
                for row in rows:
                    race_date = row['race_date']
                    array_date = race_date.split('/')
                    month = int(array_date[1])
                    if (month >= from_m) and (month <= to_m):
                        day = int(array_date[0])
                        if (day >= from_d) and (day <= to_d):
                            race_No = int(row['race_No'])
                            if (race_No >= from_no) and (race_No <= to_no):
                                horse_code = row['horse_code']
                                if horse_code not in horseCodeList:
                                    horseCodeList.append(row['horse_code'])
            else:
                common.log('table[' + tableName + '] not exist')
        print('horseCodeList count:', len(horseCodeList))

        loadedHorseCodeList = self.__getLoadedHorseCodeList()
        print('loadedHorseCodeList count:', len(loadedHorseCodeList))

        urlList = []
        n = 0
        for code in horseCodeList:
            n += 1
            # if code not in loadedHorseCodeList:
            # urlList.append(HORSE_URL_PRE + code + HORSE_URL_EX)
        print('n=', n)
        urlList.append(HORSE_URL_PRE + 'C329' + HORSE_URL_EX)
        return urlList


singleton_url = UrlManager()

