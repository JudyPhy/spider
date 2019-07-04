from common import common
import datetime

RECENT_COUNT = 90


def getTrainerRecords(trainer, race_results_rows):
    trainer_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_trainer = row['trainer'].split('(')
            cur_trainer = array_trainer[0].strip()
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


def getTrainerRecentRecords(race_date, trainer, race_results_rows):
    cur_year = int(race_date[: len(race_date) - 4])
    cur_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
    cur_day = int(race_date[len(race_date) - 2:])
    cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
    before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
    trainer_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_trainer = row['trainer'].split('(')
            cur_trainer = array_trainer[0].strip()
            cur_date = row['race_date']
            if (plc not in common.words) and (cur_trainer == trainer) and (int(cur_date) <= int(before_N_date)):
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


def getTrainerFavRecords(trainer, race_results_rows):
    trainer_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_trainer = row['trainer'].split('(')
            cur_trainer = array_trainer[0].strip()
            if (plc not in common.words) and (cur_trainer == trainer):
                cur_odds = float(row['win_odds'])
                isFav = common.IsLowestOdds(cur_odds, dict)
                if isFav:
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


def getJockeyRecentRecords(race_date, jockey, race_results_rows):
    cur_year = int(race_date[: len(race_date) - 4])
    cur_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
    cur_day = int(race_date[len(race_date) - 2:])
    cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
    before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
    jockey_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            cur_date = row['race_date']
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


def getJockeyFavRecords(jockey, race_results_rows):
    jockey_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if (plc not in common.words) and (cur_jockey == jockey):
                cur_odds = float(row['win_odds'])
                isFav = common.IsLowestOdds(cur_odds, dict)
                if isFav:
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



