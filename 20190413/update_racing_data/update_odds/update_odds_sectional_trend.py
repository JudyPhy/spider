import datetime
from db.db import singleton_ResultsDb
from db.db import singleton_ScrubDb
from config.myconfig import singleton_cfg
from common import common

base_time_odds = {}  # race_No & [base_time, horse_No & odds]

def __parseRaceStartTime(race_time):
    array_race_time = race_time.split(':')
    if len(array_race_time) == 2:
        race_start_hour = int(array_race_time[0])
        race_start_min = int(array_race_time[1])
    else:
        race_start_hour = 0
        race_start_min = 0
    return race_start_hour, race_start_min


def __getDeltaSeconds(race_start_time):
    race_date = singleton_cfg.getRaceDate()
    race_start_year = int(race_date[: len(race_date) - 4])
    race_start_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
    race_start_day = int(race_date[len(race_date) - 2:])
    race_start_hour, race_start_min = __parseRaceStartTime(race_start_time)
    d_end = datetime.datetime(race_start_year, race_start_month, race_start_day, race_start_hour, race_start_min, 0)
    d_start = datetime.datetime.now()
    delta_time = d_end - d_start
    return delta_time.total_seconds()


def __toDateTime(time_str):  # time_str: %Y-%m-%d %H:%M:%S
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def __getOdds(race_No, targetTime):
    race_date = singleton_cfg.getRaceDate()
    year = race_date[: len(race_date) - 4]
    tableName = common.PLA_ODDS_TABLE.replace('{0}', year)
    if singleton_ScrubDb.table_exists(tableName):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date=%s and race_no=%s'.format(tableName), (race_date, race_No))
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        win_odds_dict = {}  # horse_No & {update_time & odds}
        for row in rows:
            horse_No = row['horse_no']
            if horse_No not in win_odds_dict.keys():
                win_odds_dict[horse_No] = {}
            win_update_time = row['win_update_time']
            if win_update_time != '':
                update_time = __toDateTime(win_update_time)
                win_odds_dict[horse_No][update_time] = row['win_odds']

        odds_dict = {}  # horse_No & odds
        for horse_No, dict in win_odds_dict.items():
            prev_time = None
            time_sorted_list = sorted(win_odds_dict[horse_No].keys())
            for time in time_sorted_list:
                if targetTime >= time:
                    prev_time = time
                elif targetTime < time:
                    break
            odds_dict[horse_No] = float(dict[prev_time])
        return odds_dict
    else:
        print('table[', tableName, '] not exist')
        return {}


def __getTimeBaseOdds(today_race_time):
    for race_No, timeArray in today_race_time.items():
        delta_sec = __getDeltaSeconds(timeArray[0])
        if race_No not in base_time_odds.keys():
            now = datetime.datetime.now()
            odds_dict = __getOdds(race_No, now)
            base_time_odds[race_No] = [now, odds_dict]
        if delta_sec <= 60*10:
            odds_dict = __getOdds(race_No, timeArray[1])
            base_time_odds[race_No] = [timeArray[1], odds_dict]

    # print(base_time_odds[1])
    # for race_No, dict in base_time_odds.items():
    #     print(race_No, dict)
    return base_time_odds


# today_race_time: race_No & [start_time, before10_time]
def updateOddsSectionalTrend(today_table_dict, today_race_time):
    base_time_odds_dict = __getTimeBaseOdds(today_race_time)    # race_No & [base_time, horse_No & odds]
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if 'model3' not in update_table:
            continue
        if update_table in today_table_dict.keys():
            today_table = today_table_dict[update_table]
            for race_no, dict in today_table.items():
                for horse_no, row in dict.items():
                    if (race_no in base_time_odds_dict.keys()) and (horse_no in base_time_odds_dict[race_no][1].keys()):
                        base_odds = base_time_odds_dict[race_no][1][horse_no]
                        cur_odds = row['win_odds']
                        odds_trend = (cur_odds - base_odds)/base_odds
                        singleton_ResultsDb.cursor.execute('update {} set odd_wave=%s where race_no=%s and horse_no=%s'.format(update_table),
                                                           (odds_trend, race_no, horse_no))
                        singleton_ResultsDb.connect.commit()
                        # print('update odds wave:', race_no, horse_no, base_odds, cur_odds)
                    else:
                        common.log("[odds_sectional_trend]don't find horse[" + str(horse_no) + '] in race[' + str(race_no) + ']')
