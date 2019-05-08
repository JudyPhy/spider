from common import common
from db.database import singleton_Scrub_DB


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


def __getCls(cls_dict, race_date_No):
    if race_date_No in cls_dict.keys():
        return cls_dict[race_date_No]
    print("class can't find", race_date_No)
    return ''


# race_No_dict: race_date_id & race_No
def __getClsDict(race_No_dict):
    cls_dict = {}    # race_date_No & cls
    if singleton_Scrub_DB.table_exists(common.HORSE_RACE_TABLE):
        singleton_Scrub_DB.cursor.execute('select race_date,class,race_id from {}'.format(common.HORSE_RACE_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            array_date = row['race_date'].split('/')
            year = array_date[2]
            if len(year) == 2:
                year = '20' + year
            race_date_id = year + array_date[1] + array_date[0] + common.toThreeDigitStr(row['race_id'])
            if race_date_id in race_No_dict.keys():
                race_date_No = year + array_date[1] + array_date[0] + common.toDoubleDigitStr(race_No_dict[race_date_id])
                if race_date_No not in cls_dict.keys():
                    cls_dict[race_date_No] = ''
                cls_dict[race_date_No] = row['class'].strip()
    return cls_dict


def __getRaceNoDict(results_rows):
    race_No_dict = {}   # race_date_id & race_No
    for race_date_No, horse_dict in results_rows.items():
        race_date = race_date_No[:len(race_date_No) - 2]
        for horse_code, row in horse_dict.items():
            race_date_id = race_date + common.toThreeDigitStr(row['race_id'])
            if race_date_id not in race_No_dict.keys():
                race_No_dict[race_date_id] = row['race_No']
            break
    return race_No_dict


# results_rows: race_date_No & {horse_code & row}
# plc_dict: race_date_No & {horse_code & plc}
def getHorseClsRecord(raceCard_rows, results_rows, plc_dict):
    race_No_dict = __getRaceNoDict(results_rows)    # race_date_id & race_No
    cls_dict = __getClsDict(race_No_dict)  # race_date_No & cls

    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    cls_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    temp_plc_record = {}  # horse_code & {cls & [No1, No2, No3, No4, All]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in cls_record_dict.keys():
            cls_record_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            cls = __getCls(cls_dict, race_date_No)

            # 赛前
            if (horse_code in temp_plc_record.keys()) and (cls in temp_plc_record[horse_code].keys()):
                record = temp_plc_record[horse_code][cls]
                cls_record_dict[race_date_No][horse_code] = [record[0], record[1], record[2], record[3], record[4]]
            else:
                cls_record_dict[race_date_No][horse_code] = [0, 0, 0, 0, 0]

            # 赛后
            if horse_code not in temp_plc_record.keys():
                temp_plc_record[horse_code] = {}
            if cls not in temp_plc_record[horse_code].keys():
                temp_plc_record[horse_code][cls] = [0, 0, 0, 0, 0]
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                if int(plc) == 1:
                    temp_plc_record[horse_code][cls][0] += 1
                elif int(plc) == 2:
                    temp_plc_record[horse_code][cls][1] += 1
                elif int(plc) == 3:
                    temp_plc_record[horse_code][cls][2] += 1
                elif int(plc) == 4:
                    temp_plc_record[horse_code][cls][3] += 1
                temp_plc_record[horse_code][cls][4] += 1

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, cls, plc)
            #     print(temp_plc_record[horse_code])
            #     print(cls_record_dict[race_date_No][horse_code])
    return cls_record_dict

