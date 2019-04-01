from config.myconfig import singleton_cfg
from common import common
from db.db import singleton_ScrubDb

BASE_HORSE_URL = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseNo='

LOST_FILE_NAME = 'lost_horse_code.csv'


class UrlManager(object):

    def __getLoadedHorseCodeList(self, race_date):
        codeList = []
        year = race_date[: len(race_date) - 4]
        tableName = singleton_cfg.getTargetTable().replace('{0}', year)
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select code from {} where race_date=%s'.format(tableName), race_date)
            rows = singleton_ScrubDb.cursor.fetchall()
            for row in rows:
                code = row['code'].strip()
                if code not in codeList:
                    codeList.append(code)
        return codeList

    def __getTodayHorseCodeList(self, race_date):
        codeList = []
        year = race_date[: len(race_date) - 4]
        tableName = singleton_cfg.getRaceCardTable().replace('{0}', year)
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select horse_code from {} where race_date=%s'.format(tableName),
                                             race_date)
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                if row['horse_code'] not in codeList:
                    codeList.append(row['horse_code'])
        else:
            print('Table[', tableName, '] not exist')
        return codeList

    def getUrlList(self):
        race_date = singleton_cfg.getRaceDate()
        today_horse_list = self.__getTodayHorseCodeList(race_date)
        common.log('[urlManager] today horse_code count=' + str(len(today_horse_list)))

        loaded_horse_list = self.__getLoadedHorseCodeList(race_date)
        common.log('[urlManager] loaded horse_code count=' + str(len(loaded_horse_list)))

        urlList = []
        for code in today_horse_list:
            if code not in loaded_horse_list:
                u = BASE_HORSE_URL + code
                urlList.append(u)
        return urlList


singleton_url = UrlManager()

