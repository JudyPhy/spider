from common import common


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


# plc_dict: race_date_No & {horse_code & plc}
def getHorseSiteRecord(raceCard_rows, plc_dict):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    site_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    temp_plc_record = {}  # horse_code & {site & [No1, No2, No3, No4, All]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in site_record_dict.keys():
            site_record_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            site = row['site'].replace(' ', '')

            # 赛前
            if (horse_code in temp_plc_record.keys()) and (site in temp_plc_record[horse_code].keys()):
                record = temp_plc_record[horse_code][site]
                site_record_dict[race_date_No][horse_code] = [record[0], record[1], record[2], record[3], record[4]]
            else:
                site_record_dict[race_date_No][horse_code] = [0, 0, 0, 0, 0]

            # 赛后
            if horse_code not in temp_plc_record.keys():
                temp_plc_record[horse_code] = {}
            if site not in temp_plc_record[horse_code].keys():
                temp_plc_record[horse_code][site] = [0, 0, 0, 0, 0]
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                if int(plc) == 1:
                    temp_plc_record[horse_code][site][0] += 1
                elif int(plc) == 2:
                    temp_plc_record[horse_code][site][1] += 1
                elif int(plc) == 3:
                    temp_plc_record[horse_code][site][2] += 1
                elif int(plc) == 4:
                    temp_plc_record[horse_code][site][3] += 1
                temp_plc_record[horse_code][site][4] += 1
    return site_record_dict

