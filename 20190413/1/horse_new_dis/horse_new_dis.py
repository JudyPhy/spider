from common import common


def __getPlc(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        plc = results_rows[race_date_No][horse_code]['plc'].replace('DH', '').strip()
        return plc
    return ''


def getHorseNewDis(raceCard_rows, results_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    new_dis_dict = {}  # race_date_No & {horse_code & new_dis}
    temp_dis = {}  # horse_code & [dis1, dis2, dis3, dis4]
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in new_dis_dict.keys():
            new_dis_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            distance = int(row['distance'])

            # 赛前
            new_dis = False
            if (horse_code in temp_dis.keys()) and (len(temp_dis[horse_code]) == 4):
                new_dis = True
                for prev_dis in temp_dis[horse_code]:
                    if prev_dis >= (distance * 0.8):
                        new_dis = False
                        break
            new_dis_dict[race_date_No][horse_code] = new_dis

            # 赛后
            plc = __getPlc(race_date_No, horse_code, results_rows)
            if plc in common.words:
                continue
            if horse_code not in temp_dis.keys():
                temp_dis[horse_code] = []
            temp_dis[horse_code].insert(0, distance)
            temp_dis[horse_code] = temp_dis[horse_code][:4]

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, distance)
            #     print(temp_dis[horse_code])
            #     print(new_dis_dict[race_date_No][horse_code])
    return new_dis_dict

