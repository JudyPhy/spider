from common import common


def getNewDis(horse_code, distance, race_results_rows):
    sort_race_date_No = sorted(list(race_results_rows.keys()))
    sort_race_date_No.reverse()
    array_prev_4_race = []
    for race_date_No in sort_race_date_No:
        dict = race_results_rows[race_date_No]
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


