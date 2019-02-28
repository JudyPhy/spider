###     horse和trainer合作的次数统计     ###
from common import common


def getHorseTrainerRaceCount(history_rows):
    # 按比赛日期排序
    race_rows = {}  # new_race_id & [row, row, ...]
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in race_rows.keys():
            race_rows[new_race_id] = []
        race_rows[new_race_id].append(row)
    race_id_sorted_list = sorted(race_rows.keys())
    # 计算trainer和horse合作的次数
    ht_date_dict = {}   # horse__trainer & [all_count, before3_count]
    ht_count_dict = {}  # new_race_id & {horse_code & [jt_all_count, jt_before3_count]}
    for race_id in race_id_sorted_list:
        curRaceRows = race_rows[race_id]
        if race_id not in ht_count_dict.keys():
            ht_count_dict[race_id] = {}

        for row in curRaceRows:
            horse_code = row['horse_code']
            ht = row['horse_code'].strip() + '__' + row['trainer'].strip()
            # 赛前
            if ht in ht_date_dict.keys():
                ht_count_dict[race_id][horse_code] = ht_date_dict[ht]
            else:
                ht_count_dict[race_id][horse_code] = [0, 0]

            # 赛后累加
            if ht not in ht_date_dict.keys():
                ht_date_dict[ht] = [0, 0]
            all_count = ht_date_dict[ht][0]
            all_count_before3 = ht_date_dict[ht][1]
            if row['plc'] not in common.words:
                all_count += 1
                plc = int(row['plc'].replace('DH', ''))
                if plc <= 3 and plc >= 1:
                    all_count_before3 += 1
            ht_date_dict[ht] = [all_count, all_count_before3]
        # print('\n', ht_date_dict)
        # print(ht_count_dict[race_id])
    return ht_count_dict





