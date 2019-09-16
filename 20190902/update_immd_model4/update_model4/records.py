from common import common

RECENT_COUNT = 6


def getTrainerRecords(trainer, race_results_rows):
    trainer_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            cur_trainer = row['trainer'].strip()
            if (plc not in common.words) and (cur_trainer == trainer):
                trainer_records[4] += 1
                if int(plc) == 1:
                    trainer_records[0] += 1
                elif int(plc) == 2:
                    trainer_records[1] += 1
                elif int(plc) == 3:
                    trainer_records[2] += 1
                elif int(plc) == 4:
                    trainer_records[3] += 1
    return trainer_records


def getJockeyTrainerRecords(jockey__trainer, race_results_rows):
    jockey_trainer_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            cur_trainer = row['trainer'].strip()
            cur_jockey__trainer = cur_jockey + '__' + cur_trainer
            if (plc not in common.words) and (cur_jockey__trainer == jockey__trainer):
                jockey_trainer_records[4] += 1
                if int(plc) == 1:
                    jockey_trainer_records[0] += 1
                elif int(plc) == 2:
                    jockey_trainer_records[1] += 1
                elif int(plc) == 3:
                    jockey_trainer_records[2] += 1
                elif int(plc) == 4:
                    jockey_trainer_records[3] += 1
    return jockey_trainer_records


def getJockeyRecords(jockey, race_results_rows):
    jockey_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if (plc not in common.words) and (cur_jockey == jockey):
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


def getJockeyRecentRecords(jockey, race_results_rows):
    sort_race_date_No_list = sorted(list(race_results_rows.keys()))
    sort_race_date_No_list.reverse()
    jockey_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    race_date_list = []
    for race_date_No in sort_race_date_No_list:
        race_date = race_date_No[: len(race_date_No) - 2]
        dict = race_results_rows[race_date_No]
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if (plc not in common.words) and (cur_jockey == jockey):
                if race_date not in race_date_list:
                    race_date_list.append(race_date)
                if len(race_date_list) > RECENT_COUNT:
                    return jockey_records
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


def getDrawRecords(draw, race_results_rows):
    draw_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            cur_draw = row['draw']
            if (plc not in common.words) and (int(cur_draw) == draw):
                draw_records[4] += 1
                if int(plc) == 1:
                    draw_records[0] += 1
                elif int(plc) == 2:
                    draw_records[1] += 1
                elif int(plc) == 3:
                    draw_records[2] += 1
                elif int(plc) == 4:
                    draw_records[3] += 1
    return draw_records



