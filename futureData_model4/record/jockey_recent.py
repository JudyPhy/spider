from common import common

RECENT_COUNT = 6


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


def __getRecentRecord(jockey, race_date, jockey_plc_dict):
    if jockey in jockey_plc_dict.keys():
        sort_date_list = sorted(jockey_plc_dict[jockey].keys())
        sort_date_list.reverse()
        flag = False
        count = 0
        record = [0, 0, 0, 0, 0]
        for sub_race_date in sort_date_list:
            if sub_race_date == race_date:
                flag = True
            elif flag:
                record[0] += jockey_plc_dict[jockey][race_date][0]
                record[1] += jockey_plc_dict[jockey][race_date][1]
                record[2] += jockey_plc_dict[jockey][race_date][2]
                record[3] += jockey_plc_dict[jockey][race_date][3]
                record[4] += jockey_plc_dict[jockey][race_date][4]
                count += 1
                if count >= RECENT_COUNT:
                    flag = False
                    break
        return record
    else:
        return [-1, -1, -1, -1, -1]


# plc_dict: race_date_No & {horse_code & plc}
def getJockeyRecent(raceCard_rows, plc_dict):
    jockey_plc_dict = {}  # jockey & {race_date & [No1, No2, No3, No4, Fail]}
    for row in raceCard_rows:
        array_jockey = row['jockey'].split('(')
        jockey = array_jockey[0].strip()
        if jockey not in jockey_plc_dict.keys():
            jockey_plc_dict[jockey] = {}
        race_date = row['race_date']
        if race_date not in jockey_plc_dict[jockey].keys():
            jockey_plc_dict[jockey][race_date] = [0, 0, 0, 0, 0]
        horse_code = row['horse_code'].strip()
        race_date_No = race_date + common.toDoubleDigitStr(row['race_No'])
        plc = __getPlc(race_date_No, horse_code, plc_dict)
        if plc not in common.words:
            if int(plc) == 1:
                jockey_plc_dict[jockey][race_date][0] += 1
            elif int(plc) == 2:
                jockey_plc_dict[jockey][race_date][1] += 1
            elif int(plc) == 3:
                jockey_plc_dict[jockey][race_date][2] += 1
            elif int(plc) == 4:
                jockey_plc_dict[jockey][race_date][3] += 1
            elif int(plc) > 4:
                jockey_plc_dict[jockey][race_date][4] += 1

    jockey_recent_dict = {}  # race_date & {jockey & [No1, No2, No3, No4, Fail]}
    for row in raceCard_rows:
        race_date = row['race_date']
        if race_date not in jockey_recent_dict.keys():
            jockey_recent_dict[race_date] = {}
        array_jockey = row['jockey'].split('(')
        jockey = array_jockey[0].strip()
        jockey_recent_dict[race_date][jockey] = __getRecentRecord(jockey, race_date, jockey_plc_dict)
    return jockey_recent_dict

