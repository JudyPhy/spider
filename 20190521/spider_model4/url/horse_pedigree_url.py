from db.db import singleton_ScrubDb
from url.horse_race_url import HorseRaceUrl
from url.race_results_url import RaceResultsUrl
import datetime
from common import common


class HorsePedigreeUrl(object):

    BASE_URL = 'https://racing.hkjc.com/racing/english/racing-info/newhorse-ajax.asp?raceDate={0}&raceNo={1}&brandNo={2}'

    EXPORT_TABLE = 'ee_horse_pedigree'

    def __getRaceNo(self, race_date, race_id, race_date_id_No_dict):
        if (race_date in race_date_id_No_dict.keys()) and (race_id in race_date_id_No_dict[race_date].keys()):
            return race_date_id_No_dict[race_date][race_id]
        # 手动查询到的raceNo
        manual_dict = {}
        manual_dict['20070624'] = {699:3}
        manual_dict['20070617'] = {693:8}
        manual_dict['20070702'] = {716:1}
        if (race_date in manual_dict.keys()) and (race_id in manual_dict[race_date].keys()):
            return manual_dict[race_date][race_id]
        print("horse pedigree can't find race_No:", race_date, race_id)
        return 0

    def __getFirstRaceInfo(self, horse_code, race_date_id_No_dict):
        today = datetime.datetime.now()
        race_date = str(today.year) + common.toDoubleDigitStr(today.month) + common.toDoubleDigitStr(today.day)
        race_no = 0
        horse_race_table = HorseRaceUrl().EXPORT_TABLE
        if singleton_ScrubDb.table_exists(horse_race_table):
            singleton_ScrubDb.cursor.execute('select race_date, race_id from {} where code=%s'.format(horse_race_table), horse_code)
            race_rows = singleton_ScrubDb.cursor.fetchall()
            for row in race_rows:
                race_id = row['race_id']
                if 'Overseas' != race_id:
                    array_date = row['race_date'].split('/')
                    str_year = array_date[2]
                    if len(str_year) == 2:
                        str_year = '20' + str_year
                    race_date_ymd = str_year + array_date[1] + array_date[0]   # 20080403
                    race_No = self.__getRaceNo(race_date_ymd, int(race_id), race_date_id_No_dict)
                    if race_No != 0:   # 20080403
                        if int(race_date_ymd) < int(race_date):
                            race_date = race_date_ymd
                            race_no = race_No
        # print('horse[', horse_code, '] first race info:', race_date, race_no)
        return race_date, race_no

    def getUrl(self, horse_code, race_date_id_No_dict):
        race_date, race_No = self.__getFirstRaceInfo(horse_code, race_date_id_No_dict)
        return self.BASE_URL.replace('{0}', race_date).replace('{1}', str(race_No)).replace('{2}', horse_code)

    def getLoadedHorseCodeList(self):
        loaded_code_list = []
        if singleton_ScrubDb.table_exists(self.EXPORT_TABLE):
            singleton_ScrubDb.cursor.execute('select code from {}'.format(self.EXPORT_TABLE))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                horse_code = row['code'].strip()
                if horse_code not in loaded_code_list:
                    loaded_code_list.append(horse_code)
            print('loaded horse pedigree count=', len(loaded_code_list))
        return loaded_code_list

