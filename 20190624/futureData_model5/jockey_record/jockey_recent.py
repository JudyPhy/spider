from common import common
import datetime

RECENT_COUNT = 90


def __getJockey(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array_jockey = immd_info_dict[race_date_No][horse_No]['jockey'].split('(')
        return array_jockey[0].strip()
    return ''


def __getJockeyRecentRecords(jockey, before_N_date, history_raceResults_rows):
    jockey_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        cur_date = race_date_No[: len(race_date_No) - 2]
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if (plc not in common.words) and (cur_jockey == jockey) and (int(cur_date) >= int(before_N_date)):
                jockey_records[4] += 1
                if int(plc) == 1:
                    jockey_records[0] += 1
                elif int(plc) == 2:
                    jockey_records[1] += 1
                elif int(plc) == 3:
                    jockey_records[2] += 1
                elif int(plc) == 4:
                    jockey_records[3] += 1
    return jockey_records


def GetJockeyRecent(future_raceCard_rows, immd_info_dict, history_raceResults_rows):
    jockey_recent_dict = {}  # jockey & [No1, No2, No3, No4, All]
    jockey_date_dict = {}   # jockey & before_N_date
    for race_date_No, dict in future_raceCard_rows.items():
        cur_race_date = race_date_No[: len(race_date_No) - 2]
        cur_year = int(cur_race_date[: len(cur_race_date) - 4])
        cur_month = int(cur_race_date[len(cur_race_date) - 4: len(cur_race_date) - 2])
        cur_day = int(cur_race_date[len(cur_race_date) - 2:])
        cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
        before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
        for horse_No, row in dict.items():
            jockey = __getJockey(race_date_No, horse_No, immd_info_dict)
            if jockey == '':
                array_jockey = row['jockey'].split('(')
                jockey = array_jockey[0].strip()
            if jockey not in jockey_date_dict:
                jockey_date_dict[jockey] = before_N_date
    for jockey, before_N_date in jockey_date_dict.items():
        jockey_recent_dict[jockey] = __getJockeyRecentRecords(jockey, before_N_date, history_raceResults_rows)
    return jockey_recent_dict

