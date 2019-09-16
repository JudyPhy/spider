from common import common


def GetHorseSiteRecord(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_site_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    temp_horse_site_record = {}  # horse_code & {site & [No1, No2, No3, No4, All]}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_site_record_dict.keys():
            horse_site_record_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    cur_site = sort_history_raceResults_rows[race_date_No][horse_code]['site'].replace(' ', '')
                    if horse_code not in temp_horse_site_record.keys():
                        temp_horse_site_record[horse_code] = {}
                    if cur_site not in temp_horse_site_record[horse_code].keys():
                        temp_horse_site_record[horse_code][cur_site] = [0, 0, 0, 0, 0]
                    # before
                    cur_record = temp_horse_site_record[horse_code][cur_site]
                    horse_site_record_dict[race_date_No][horse_code] = [cur_record[0], cur_record[1], cur_record[2], cur_record[3], cur_record[4]]
                    # after
                    temp_horse_site_record[horse_code][cur_site][4] += 1
                    if int(cur_plc) == 1:
                        temp_horse_site_record[horse_code][cur_site][0] += 1
                    elif int(cur_plc) == 2:
                        temp_horse_site_record[horse_code][cur_site][1] += 1
                    elif int(cur_plc) == 3:
                        temp_horse_site_record[horse_code][cur_site][2] += 1
                    elif int(cur_plc) == 4:
                        temp_horse_site_record[horse_code][cur_site][3] += 1
    return horse_site_record_dict

