from common import common


def __getDrawRecords(draw, history_raceResults_rows):
    draw_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
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


def GetDrawRecord(future_raceCard_rows, history_raceResults_rows):
    draw_record_dict = {}  # draw & [No1, No2, No3, No4, All]
    draw_list = []
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            draw = int(row['draw'])
            if draw not in draw_list:
                draw_list.append(draw)
    for draw in draw_list:
        draw_record_dict[draw] = __getDrawRecords(draw, history_raceResults_rows)
    return draw_record_dict

