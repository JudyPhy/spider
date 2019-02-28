from config.myconfig import singleton as singleton_cfg
from common import common
from db.db import singleton_ScrubDb
import datetime

BASE_URL = 'https://racing.hkjc.com/racing/english/racing-info/newhorse-ajax.asp?raceDate={0}&raceNo={1}&brandNo={2}'

RESULTS_TABLE = 'f_race_results_YEAR'

HORSE_RACE_TABLE = 'c_horse_race_info'


class UrlManager(object):

    def __getLoadedHorseCodeList(self):
        codeList = []
        tableName = singleton_cfg.getTargetTable()
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select code from {}'.format(tableName))
            rows = singleton_ScrubDb.cursor.fetchall()
            for row in rows:
                horse_code = row['code'].strip()
                if horse_code not in codeList:
                    codeList.append(horse_code)
        return codeList

    def __getAllResults(self):
        raceNoDict = {}  # race_date & {race_id & race_No}
        spider_horse_code_list = []
        for year in range(2007, 2020):
            tableName = RESULTS_TABLE.replace('YEAR', str(year))
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute('select horse_code,race_date,race_id,race_No from {}'.format(tableName))
                rows = singleton_ScrubDb.cursor.fetchall()
                singleton_ScrubDb.connect.commit()
                for row in rows:
                    horse_code = row['horse_code']
                    if (year >= 2014) and (horse_code not in spider_horse_code_list):
                        spider_horse_code_list.append(horse_code)

                    array_date = row['race_date'].split('/')
                    str_year = array_date[2]
                    race_date = str_year[len(str_year) - 2:] + array_date[1] + array_date[0]
                    if race_date not in raceNoDict.keys():
                        raceNoDict[race_date] = {}
                    race_id = row['race_id']
                    if race_id not in raceNoDict[race_date].keys():
                        raceNoDict[race_date][race_id] = row['race_No']
        return spider_horse_code_list, raceNoDict

    def __getAllHorseRace(self):
        horseRace = []
        if singleton_ScrubDb.table_exists(HORSE_RACE_TABLE):
            singleton_ScrubDb.cursor.execute('select code,race_date,race_id from {}'.format(HORSE_RACE_TABLE))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            horseRace += rows
        return horseRace

    def __getRaceNo(self, race_date, race_id, raceNoDict):
        # print(race_date in raceNoDict.keys())
        # if race_date in raceNoDict.keys():
        #     print(race_id in raceNoDict[race_date].keys())
        if (race_date in raceNoDict.keys()) and (race_id in raceNoDict[race_date].keys()):
            return raceNoDict[race_date][race_id]
        # 手动查询到的raceNo
        manual_dict = {}
        manual_dict['070624'] = {699:3}
        manual_dict['070617'] = {693:8}
        manual_dict['070702'] = {716:1}
        if (race_date in manual_dict.keys()) and (race_id in manual_dict[race_date].keys()):
            return manual_dict[race_date][race_id]
        return 0

    def getUrlList(self):
        spider_horse_code_list, raceNoDict = self.__getAllResults()
        print('horse count(>=2014) => ', len(spider_horse_code_list))

        codeDict = {}   # horse_code & [race_date, race_no]
        horseRace_rows = self.__getAllHorseRace()
        for row in horseRace_rows:
            horse_code = row['code'].strip()
            race_id = row['race_id']
            if (horse_code not in spider_horse_code_list) or (race_id == 'Overseas'):
                continue
            array_date = row['race_date'].split('/')
            str_year = array_date[2]
            race_date = str_year[len(str_year) - 2:] + array_date[1] + array_date[0]  # 080203
            race_no = self.__getRaceNo(race_date, int(race_id), raceNoDict)
            if race_no == 0:
                print('race_no=0:', horse_code, race_date, race_id)
                continue
            if horse_code not in codeDict.keys():
                codeDict[horse_code] = [race_date, race_no]
            if int(race_date) < int(codeDict[horse_code][0]):
                codeDict[horse_code] = [race_date, race_no]
        print('codeDict:', len(codeDict))

        # if len(codeDict) < len(code_list):
        #     less = []
        #     for code in code_list:
        #         if code not in codeDict.keys():
        #             less.append(code)
        #     print(less)

        # 剔除已爬取到的马匹code
        urlList = []
        loaded_horse_code = self.__getLoadedHorseCodeList()
        print('loaeded count:', len(loaded_horse_code))
        error = []
        for code, info in codeDict.items():
            if code not in loaded_horse_code:
                u = BASE_URL.replace('{0}', '20' + str(info[0])).replace('{1}', str(info[1])).replace('{2}', code)
                urlList.append(u)
            else:
                error.append(code)
        print('error:', error)
        return urlList


singleton_url = UrlManager()

