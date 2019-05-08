from common import common
import datetime


def __getRest(prev_race_date, cur_race_date):
    prev_year = int(prev_race_date[: (len(prev_race_date) - 4)])
    prev_month = int(prev_race_date[(len(prev_race_date) - 4): (len(prev_race_date) - 2)])
    prev_day = int(prev_race_date[(len(prev_race_date) - 2):])
    cur_year = int(cur_race_date[: (len(cur_race_date) - 4)])
    cur_month = int(cur_race_date[(len(cur_race_date) - 4): (len(cur_race_date) - 2)])
    cur_day = int(cur_race_date[(len(cur_race_date) - 2):])
    prev_time = datetime.datetime(prev_year, prev_month, prev_day)
    cur_time = datetime.datetime(cur_year, cur_month, cur_day)
    deltaDays = (cur_time - prev_time).days
    return deltaDays


def getHorseRest(raceCard_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    rest_dict = {}  # race_date_No & {horse_code & rest}
    temp_date = {}  # horse_code & prev_date
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in rest_dict.keys():
            rest_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            race_date = row['race_date']

            # 赛前
            if horse_code not in temp_date.keys():
                rest_dict[race_date_No][horse_code] = 0
            else:
                rest = __getRest(temp_date[horse_code], race_date)
                rest_dict[race_date_No][horse_code] = rest

            # 赛后
            temp_date[horse_code] = race_date

            # if 'V082' == horse_code:
            #     print('\n', race_date_No)
            #     print(temp_date[horse_code])
            #     print(rest_dict[race_date_No][horse_code])
    return rest_dict

