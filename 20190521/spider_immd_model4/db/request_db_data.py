from db.db import singleton_ScrubDb
from common import common
import datetime


def RequestRaceStartTime():
    race_start_time_dict = {}   # race_date_No & start_time
    if singleton_ScrubDb.table_exists(common.FUTURE_RACE_CARD_TABLE):
        today = datetime.datetime.now()
        today_date = str(today.year) + common.toDoubleDigitStr(today.month) + common.toDoubleDigitStr(today.day)
        singleton_ScrubDb.cursor.execute('select * from {} where race_date>=%s'.format(common.FUTURE_RACE_CARD_TABLE), today_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_date = row['race_date']
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            race_start_time_dict[race_date_No] = row['race_time']
    else:
        common.log('table[' + common.FUTURE_RACE_CARD_TABLE + '] not exist')
    # print('race start time=', race_start_time_dict)
    return race_start_time_dict



