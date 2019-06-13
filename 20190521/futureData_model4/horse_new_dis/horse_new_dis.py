from common import common


def __getNewDis(horse_code, distance, history_raceResults_rows):
    sort_race_date_No = sorted(list(history_raceResults_rows.keys()))
    sort_race_date_No.reverse()
    array_prev_4_race = []
    for race_date_No in sort_race_date_No:
        dict = history_raceResults_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                cur_distance = int(dict[horse_code]['distance'])
                array_prev_4_race.append(cur_distance)
                if len(array_prev_4_race) == 4:
                    break
    if len(array_prev_4_race) == 4:
        for prev_dis in array_prev_4_race:
            if prev_dis >= (distance * 0.8):
                return False
        return True
    return False


def GetHorseNewDis(future_raceCard_rows, history_raceResults_rows):
    new_dis_dict = {}  # race_date_No & {horse_No & new_dis}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in new_dis_dict.keys():
            new_dis_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            distance = int(row['distance'])
            new_dis_dict[race_date_No][horse_No] = __getNewDis(horse_code, distance, history_raceResults_rows)
    return new_dis_dict

