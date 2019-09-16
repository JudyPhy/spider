from common import common


def __getDrawRecord(horse_code, draw, history_raceResults_rows):
    draw_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_draw = dict[horse_code]['draw']
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


def GetHorseDrawRecord(future_raceCard_rows, history_raceResults_rows):
    draw_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in draw_record_dict.keys():
            draw_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            draw = int(row['draw'])
            draw_record_dict[race_date_No][horse_No] = __getDrawRecord(horse_code, draw, history_raceResults_rows)
    return draw_record_dict

