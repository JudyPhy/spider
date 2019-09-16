from common import common


def GetHorseNewDis(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_new_dis_dict = {}  # race_date_No & {horse_code & new_dis}
    temp_horse_dis_dict = {}  # horse_code & [dis1, dis2, dis3, dis4]
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_new_dis_dict.keys():
            horse_new_dis_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_dis_dict.keys():
                        temp_horse_dis_dict[horse_code] = []
                    # before
                    cur_distance = int(row['distance'])
                    new_dis = True
                    if len(temp_horse_dis_dict[horse_code]) < 4:
                        new_dis = False
                    for prev_dis in temp_horse_dis_dict[horse_code]:
                        if prev_dis >= (cur_distance * 0.8):
                            new_dis = False
                            break
                    horse_new_dis_dict[race_date_No][horse_code] = new_dis
                    # after
                    temp_horse_dis_dict[horse_code].insert(0, cur_distance)
                    temp_horse_dis_dict[horse_code] = temp_horse_dis_dict[horse_code][:4]
    return horse_new_dis_dict

