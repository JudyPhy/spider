import datetime


def __toDateTime(time_str):  # time_str: %Y-%m-%d %H:%M:%S
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def __getSectionalTime(race_start_time):
    start_time = __toDateTime(race_start_time)
    time5 = start_time - datetime.timedelta(minutes=5)
    time10 = start_time - datetime.timedelta(minutes=10)
    time15 = start_time - datetime.timedelta(minutes=15)
    time20 = start_time - datetime.timedelta(minutes=20)
    # print(race_start_time, time5.strftime("%Y-%m-%d %H:%M"), time10.strftime("%Y-%m-%d %H:%M"), time15.strftime("%Y-%m-%d %H:%M"), time20.strftime("%Y-%m-%d %H:%M"))
    return [time5, time10, time15, time20]


def GetSectionalOddsRows(orig_immd_odds_row):
    sectional_odds_row = {}  # race_date_No & {horse_No & [odds]}
    for race_date_No, row_dict in orig_immd_odds_row.items():
        if race_date_No not in sectional_odds_row.keys():
            sectional_odds_row[race_date_No] = {}
        for horse_No, rows in row_dict.items():
            if horse_No not in sectional_odds_row[race_date_No].keys():
                sectional_odds_row[race_date_No][horse_No] = []
            year = race_date_No[: len(race_date_No) - 6]
            month = race_date_No[len(race_date_No) - 6: len(race_date_No) - 4]
            day = race_date_No[len(race_date_No) - 4: len(race_date_No) - 2]
            race_start_time = year + '-' + month + '-' + day + ' ' + rows[0]['start_time'].replace(' ', '') + ':00'  # %Y-%m-%d %H:%M:%S
            sectionalTime = __getSectionalTime(race_start_time)
            for subTime in sectionalTime:
                delta_time = datetime.datetime.now() - subTime
                delta_min_row = None
                for row in rows:
                    curTime = __toDateTime(row['update_time'])
                    if (curTime <= subTime) and ((curTime - subTime) < delta_time):
                        delta_min_row = row
                if delta_min_row:
                    if delta_min_row['exit_race'] == 1:
                        sectional_odds_row[race_date_No][horse_No].append(float(0))
                    else:
                        sectional_odds_row[race_date_No][horse_No].append(float(delta_min_row['win_odds']))
                else:
                    print('ERROR: ', delta_time)
    return sectional_odds_row





