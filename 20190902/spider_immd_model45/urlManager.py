from wpSpider import WPSpider
import datetime
from db import request_db_data
from common import common
import time
from db import pla_win_odds_db


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
    race_start_year = int(race_date[: len(race_date) - 4])
    race_start_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
    race_start_day = int(race_date[len(race_date) - 2:])
    race_start_hour, race_start_min = __parseRaceStartTime(race_start_time)
    d_end = datetime.datetime(race_start_year, race_start_month, race_start_day, race_start_hour, race_start_min, 0)
    d_start = datetime.datetime.now()
    delta_time = d_end - d_start
    return delta_time.total_seconds()


def __getSpiderRaceDateNoList(race_start_time_dict):
    race_date_No_list_less10 = []
    for race_date_No, race_start_time in race_start_time_dict.items():
        deltaSec = __getDeltaSeconds(race_date_No[:len(race_date_No) - 2], race_start_time)
        if (deltaSec > 0) and (deltaSec <= 10*60):
            race_date_No_list_less10.append(race_date_No)
    if len(race_date_No_list_less10) > 0:
        return race_date_No_list_less10
    else:
        return list(race_start_time_dict.keys())


def __raceOver(race_start_time_dict):
    over_race_list = []
    for race_date_No, race_start_time in race_start_time_dict.items():
        deltaSec = __getDeltaSeconds(race_date_No[:len(race_date_No) - 2], race_start_time)
        if deltaSec < -60*60:
            over_race_list.append(race_date_No)
    if len(over_race_list) == len(race_start_time_dict.keys()):
        return True
    else:
        return False


# {0}:2019-06-05  {1}:1
WIN_ODDS_URL = 'https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=en&date={0}&venue=st&raceno={1}'
# {0}:2019-06-05
FIRST4_URL = 'https://bet.hkjc.com/racing/pages/odds_ff.aspx?lang=en&date={0}&venue=HV'


def loop():
    while(True):
        race_start_time_dict = request_db_data.RequestRaceStartTime()
        print('future race count:', len(race_start_time_dict))
        if len(race_start_time_dict) > 0:
            while(True):
                race_date_No_list = __getSpiderRaceDateNoList(race_start_time_dict)
                for race_date_No in race_date_No_list:
                    race_year = race_date_No[: len(race_date_No) - 6]
                    race_month = race_date_No[len(race_date_No) - 6: len(race_date_No) - 4]
                    race_day = race_date_No[len(race_date_No) - 4: len(race_date_No) - 2]
                    race_date = race_year + '-' + race_month + '-' + race_day
                    race_No = int(race_date_No[len(race_date_No) - 2:])
                    wp_url = WIN_ODDS_URL.replace('{0}', race_date).replace('{1}', str(race_No))
                    spider = WPSpider(wp_url)
                    if len(spider.wpTable) > 0:
                        pla_win_odds_db.exportToDb(spider)
                if __raceOver(race_start_time_dict):
                    break
        time.sleep(0.5)

