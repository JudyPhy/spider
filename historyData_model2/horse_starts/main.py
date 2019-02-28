from common import common


def __getOnRaceStarts(rows):
    one_race_starts_dict = {}   # horse_code & [No1, No2, No3, No4, ALL]
    for row in rows:
        horse_code = row['horse_code']
        if horse_code not in one_race_starts_dict.keys():
            one_race_starts_dict[horse_code] = [0, 0, 0, 0, 0]
        if row['plc'] not in common.words:
            one_race_starts_dict[horse_code][4] += 1
            plc = int(row['plc'].replace('DH', ''))
            if plc == 1:
                one_race_starts_dict[horse_code][0] += 1
            elif plc == 2:
                one_race_starts_dict[horse_code][1] += 1
            elif plc == 3:
                one_race_starts_dict[horse_code][2] += 1
            elif plc == 4:
                one_race_starts_dict[horse_code][3] += 1
    return one_race_starts_dict


def __calculateHorseStar(history_rows):
    results_dict = {}   # new_race_id & {horse_code & [No1, No2, No3, No4, ALL]}
    sum_start_dict = {}  # horse_code & [No1, No2, No3, No4, ALL]
    # 按照比赛日期排序
    dict_race_id_rows = {}  # new_race_id & [row1, row2, ...]
    for row_orig in history_rows:
        new_race_id = int(str(row_orig['race_date']) + common.toThreeDigitStr(row_orig['race_id']))
        if new_race_id not in dict_race_id_rows.keys():
            dict_race_id_rows[new_race_id] = []
        dict_race_id_rows[new_race_id].append(row_orig)
    sorted_race_id = sorted(dict_race_id_rows.keys())
    # 计算每场比赛的starts数据
    for race_id in sorted_race_id:
        if race_id not in results_dict.keys():
            results_dict[race_id] = {}
        curRaceRows = dict_race_id_rows[race_id]

        # 赛前
        for row in curRaceRows:
            horse_code = row['horse_code']
            if horse_code in sum_start_dict.keys():
                curData = sum_start_dict[horse_code]
                results_dict[race_id][horse_code] = [curData[0], curData[1], curData[2], curData[3], curData[4]]
            else:
                results_dict[race_id][horse_code] = [0, 0, 0, 0, 0]

        # 赛后，累加本场场次
        curRace_starts_dict = __getOnRaceStarts(curRaceRows)    # horse_code & [No1, No2, No3, No4, ALL]
        for row in curRaceRows:
            horse_code = row['horse_code']
            if horse_code not in sum_start_dict.keys():
                sum_start_dict[horse_code] = [0, 0, 0, 0, 0]
            curData = curRace_starts_dict[horse_code]
            for index in range(len(sum_start_dict[horse_code])):
                sum_start_dict[horse_code][index] += curData[index]
    return results_dict, sum_start_dict


def getHorseStartsDict(history_rows):
    dict_race_start, dict_allRace_start = __calculateHorseStar(history_rows)
    return dict_race_start, dict_allRace_start
