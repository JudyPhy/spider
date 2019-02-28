###     horse和jockey合作的次数统计     ###
from common import common


def getHorseJockeyRaceCount(history_rows):
    # 按比赛日期排序
    race_rows = {}  # new_race_id & [row, row, ...]
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in race_rows.keys():
            race_rows[new_race_id] = []
        race_rows[new_race_id].append(row)
    race_id_sorted_list = sorted(race_rows.keys())
    # 计算jockey和horse合作的次数
    hj_date_dict = {}   # horse__jockey & [all_count, before3_count]
    hj_count_dict = {}  # new_race_id & {horse_code & [jt_all_count, jt_before3_count]}
    for race_id in race_id_sorted_list:
        curRaceRows = race_rows[race_id]
        if race_id not in hj_count_dict.keys():
            hj_count_dict[race_id] = {}

        for row in curRaceRows:
            horse_code = row['horse_code']
            hj = row['horse_code'].strip() + '__' + row['jockey'].strip()
            # 赛前
            if hj in hj_date_dict.keys():
                hj_count_dict[race_id][horse_code] = hj_date_dict[hj]
            else:
                hj_count_dict[race_id][horse_code] = [0, 0]

            # 赛后累加
            if hj not in hj_date_dict.keys():
                hj_date_dict[hj] = [0, 0]
            all_count = hj_date_dict[hj][0]
            all_count_before3 = hj_date_dict[hj][1]
            if row['plc'] not in common.words:
                all_count += 1
                plc = int(row['plc'].replace('DH', ''))
                if plc <= 3 and plc >= 1:
                    all_count_before3 += 1
            hj_date_dict[hj] = [all_count, all_count_before3]
        # print('\n', hj_date_dict)
        # print(hj_count_dict[race_id])
    return hj_count_dict





