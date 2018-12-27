from config.myconfig import singleton as singleton_cfg
from common import common
from db.db import singleton_ScrubDb

BASE_HORSE_URL = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseNo='

LOST_FILE_NAME = 'lost_horse_code.csv'


class UrlManager(object):

    def __getLoadedHorseCodeList(self):
        codeList = []
        tableName = singleton_cfg.getTargetTable()
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
        tableName = singleton_cfg.getSourceTable()
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select horse_code from {}'.format(tableName))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                if row['horse_code'] not in codeList:
                    codeList.append(row['horse_code'])
        common.log('[urlManager] all horse_code count=' + str(len(codeList)))

        # 剔除已爬取到的马匹code
        loaded_horse_code = self.__getLoadedHorseCodeList()
        for code in codeList:
            if code not in loaded_horse_code:
                u = BASE_HORSE_URL + code
                urlList.append(u)
        return urlList


singleton_url = UrlManager()

