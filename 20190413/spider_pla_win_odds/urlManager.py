from wpSpider import WPSpider
import datetime
from db.db import singleton_ScrubDb
from common import common
import time
from db import pla_win_odds_table


def __parseRaceStartTime(race_time):
    array_race_time = race_time.split(':')
    if len(array_race_time) == 2:
        race_start_hour = int(array_race_time[0])
        race_start_min = int(array_race_time[1])
    else:
        race_start_hour = 0
        race_start_min = 0
    return race_start_hour, race_start_min


def __getDeltaSeconds(race_date, race_start_time):
    array_race_time = race_start_time.split(':')
    if len(array_race_time) == 2:
        race_start_year = int(race_date[: len(race_date) - 4])
        race_start_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
        race_start_day = int(race_date[len(race_date) - 2:])
        race_start_hour, race_start_min = __parseRaceStartTime(race_start_time)
        d_end = datetime.datetime(race_start_year, race_start_month, race_start_day, race_start_hour, race_start_min, 0)
        d_start = datetime.datetime.now()
        delta_time = d_end - d_start
        return delta_time.total_seconds()
    return None


def __getRaceStartTime(race_date):
    race_start_time_dict = {}   # race_no & start_time
    tableName = 't_race_card_future_' + race_date[: len(race_date) - 4]
    if singleton_ScrubDb.table_exists(tableName):
        for race_no in range(1, 12):
            singleton_ScrubDb.cursor.execute('select race_time from {} where race_date=%s and race_no=%s'.format(tableName),
                                             (race_date, race_no))
            row = singleton_ScrubDb.cursor.fetchone()
            if row:
                race_start_time_dict[race_no] = row['race_time']
    else:
        common.log('table[' + tableName + '] not exist')
    print('race_date=', race_date, ' RaceStartTime=', len(race_start_time_dict))
    return race_start_time_dict


def __getRaceStartDeltaTime(race_date, race_start_time_dict):
    start_delta_time = {}   # race_No & delta_time
    for race_no, start_time in race_start_time_dict.items():
        deltaSec = __getDeltaSeconds(race_date, start_time)
        start_delta_time[race_no] = deltaSec
    return start_delta_time


def __getSpiderRaceNoList(start_delta_time_dict):
    race_no_list = []
    min_delta_time = 3 * 60 * 60    # 3小时
    for race_No, delta_time in start_delta_time_dict.items():
        if (delta_time > 0) and (delta_time < 10 * 60):  # 10分钟内爬取一场比赛
            return [race_No]
        elif delta_time < min_delta_time:
            min_delta_time = delta_time
    # 5小时内爬取所有场次比赛
    if min_delta_time < 15 * 60 * 60:
        race_no_list = list(start_delta_time_dict.keys())
    return race_no_list


def __raceOver(start_delta_time_dict):
    # print('start_delta_time_dict:', start_delta_time_dict)
    for race_No, delta_time in start_delta_time_dict.items():
        if delta_time > -60*60:  # 比赛结束1小时后停止爬取当天比赛
            return False
    return True


def loop():
    while(True):
        # today = datetime.datetime(2019, 2, 28)
        today = datetime.datetime.now()
        for deltaDay in range(5):
            detaday = datetime.timedelta(days=deltaDay)
            future = today + detaday
            race_date = str(future.year) + common.toDoubleDigitStr(future.month) + common.toDoubleDigitStr(future.day)
            print('race_date:', race_date)
            race_start_time_dict = __getRaceStartTime(race_date)
            if len(race_start_time_dict) > 0:
                common.log('\n比赛日期：' + race_date)
                while(True):
                    start_delta_time_dict = __getRaceStartDeltaTime(race_date, race_start_time_dict)    # race_No & delta_time
                    race_no_list = __getSpiderRaceNoList(start_delta_time_dict)
                    for race_no in race_no_list:
                        spider = WPSpider(race_date, race_no)
                        if len(spider.wpTable) > 0:
                            pla_win_odds_table.updatePlaOdds(spider)
                    if __raceOver(start_delta_time_dict):
                        break
            time.sleep(0.5)

