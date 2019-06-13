import datetime
from db.db import singleton_ScrubDb
from common import common
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


class RaceDeltaDays(object):

    def __getBeginDate(self, horse_code):
        now = datetime.datetime.now()
        begin_date = int(str(now.year) + common.toDoubleDigitStr(now.month) + common.toDoubleDigitStr(now.day))
        for year in range(2013, now.year + 1):
            tableName = RESULTS_TABLE.replace('{0}', str(year))
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute(
                    '''select race_date from {} where horse_code=%s'''.format(tableName), horse_code)
                all_rows = singleton_ScrubDb.cursor.fetchall()
                singleton_ScrubDb.connect.commit()
                for row in all_rows:
                    array_date = row['race_date'].split('/')
                    race_date = int(array_date[2] + array_date[1] + array_date[0])
                    if race_date < begin_date:
                        begin_date = race_date
            else:
                print('deltaDays: table[' + tableName + '] not exist')
        return begin_date

    def getDeltaDays(self, race_date, horse_code):
        begin_date = self.__getBeginDate(horse_code)
        str_start_date = str(begin_date)
        year_from = int(str_start_date[:len(str_start_date) - 4])
        month_from = int(str_start_date[len(str_start_date) - 4: len(str_start_date) - 2])
        day_from = int(str_start_date[len(str_start_date) - 2:])

        str_race_date = str(race_date)
        year_to = int(str_race_date[:len(str_race_date) - 4])
        month_to = int(str_race_date[len(str_race_date) - 4: len(str_race_date) - 2])
        day_to = int(str_race_date[len(str_race_date) - 2:])

        d_start = datetime.date(year_from, month_from, day_from)
        d_end = datetime.date(year_to, month_to, day_to)
        sumDay = d_end - d_start
        return sumDay.days


def getData(race_no, horse_no, horse_code):
    race_date = singleton_cfg.getRaceDate()
    deltaDays = RaceDeltaDays().getDeltaDays(race_date, horse_code)
    pass

