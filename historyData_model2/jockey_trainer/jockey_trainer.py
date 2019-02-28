###     jockey和trainer合作的次数统计，以天为单位统计     ###
from common import common


def getJockeyTrainerRaceCount(history_rows):
    # 按比赛日期排序
    race_rows = {}  # race_date & [row, row, ...]
    for row in history_rows:
        race_date = row['race_date']
        if race_date not in race_rows.keys():
            race_rows[race_date] = []
        race_rows[race_date].append(row)
    race_date_sorted_list = sorted(race_rows.keys())
    # 计算jockey和trainer合作的次数
    jt_date_dict = {}   # jockey__trainer & [all_count, before3_count]
    jt_count_dict = {}  # new_race_id & {horse_code & [jt_all_count, jt_before3_count]}
    for race_date in race_date_sorted_list:
        curDayRaceRows = race_rows[race_date]
        curDayCount = {}    # jt & [all_count, before3_count]
        for row in curDayRaceRows:
            race_id = int(str(race_date) + common.toThreeDigitStr(row['race_id']))
            if race_id not in jt_count_dict.keys():
                jt_count_dict[race_id] = {}
            horse_code = row['horse_code']
            array_jockey = row['jockey'].split('(')
            array_trainer = row['trainer'].split('(')
            jt = array_jockey[0].strip() + '__' + array_trainer[0].strip()
            # 赛前
            if jt in jt_date_dict.keys():
                jt_count_dict[race_id][horse_code] = jt_date_dict[jt]
            else:
                jt_count_dict[race_id][horse_code] = [0, 0]

            # 赛后统计当日次数
            if jt not in curDayCount.keys():
                curDayCount[jt] = [0, 0]
            if row['plc'] not in common.words:
                curDayCount[jt][0] += 1
                plc = int(row['plc'].replace('DH', ''))
                if plc <= 3 and plc >= 1:
                    curDayCount[jt][1] += 1
        # 将当日次数累加到总次数中
        for jt, arrayCount in curDayCount.items():
            if jt not in jt_date_dict.keys():
                jt_date_dict[jt] = [0, 0]
            all_count = jt_date_dict[jt][0] + arrayCount[0]
            all_count_before3 = jt_date_dict[jt][1] + arrayCount[1]
            jt_date_dict[jt] = [all_count, all_count_before3]
    return jt_count_dict





