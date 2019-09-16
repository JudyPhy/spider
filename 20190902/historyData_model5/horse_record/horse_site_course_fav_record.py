from common import common


def GetHorseSiteCourseFavRecord(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_site_course_fav_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    temp_horse_site_course_fav_record = {}  # horse_code & {site_course & [No1, No2, No3, No4, All]}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_site_course_fav_record_dict.keys():
            horse_site_course_fav_record_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    cur_site = sort_history_raceResults_rows[race_date_No][horse_code]['site'].replace(' ', '')
                    cur_course = sort_history_raceResults_rows[race_date_No][horse_code]['course'].strip().upper()
                    if '"' in cur_course:
                        array_course = cur_course.split('"')
                        cur_course = array_course[1].strip()
                    cur_site_course = cur_site + '_' + cur_course
                    if horse_code not in temp_horse_site_course_fav_record.keys():
                        temp_horse_site_course_fav_record[horse_code] = {}
                    if cur_site_course not in temp_horse_site_course_fav_record[horse_code].keys():
                        temp_horse_site_course_fav_record[horse_code][cur_site_course] = [0, 0, 0, 0, 0]
                    # before
                    cur_record = temp_horse_site_course_fav_record[horse_code][cur_site_course]
                    horse_site_course_fav_record_dict[race_date_No][horse_code] = [cur_record[0], cur_record[1], cur_record[2], cur_record[3], cur_record[4]]
                    # after
                    cur_odds = float(sort_history_raceResults_rows[race_date_No][horse_code]['win_odds'])
                    isFav = common.IsLowestOdds(cur_odds, sort_history_raceResults_rows[race_date_No])
                    if isFav:
                        temp_horse_site_course_fav_record[horse_code][cur_site_course][4] += 1
                        if int(cur_plc) == 1:
                            temp_horse_site_course_fav_record[horse_code][cur_site_course][0] += 1
                        elif int(cur_plc) == 2:
                            temp_horse_site_course_fav_record[horse_code][cur_site_course][1] += 1
                        elif int(cur_plc) == 3:
                            temp_horse_site_course_fav_record[horse_code][cur_site_course][2] += 1
                        elif int(cur_plc) == 4:
                            temp_horse_site_course_fav_record[horse_code][cur_site_course][3] += 1

    return horse_site_course_fav_record_dict

