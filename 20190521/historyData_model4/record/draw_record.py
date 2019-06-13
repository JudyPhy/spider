from common import common


def GetDrawRecord(sort_race_date_rows, sort_history_raceResults_rows):
    draw_record_dict = {}  # race_date & {draw & [No1, No2, No3, No4, All]}
    temp_draw_records = {}  # draw & [No1, No2, No3, No4, All]
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in draw_record_dict.keys():
            draw_record_dict[race_date] = {}
        for row in rows:
            cur_draw = int(row['draw'])
            if cur_draw not in temp_draw_records.keys():
                temp_draw_records[cur_draw] = [0, 0, 0, 0, 0]
            # before
            records = temp_draw_records[cur_draw]
            draw_record_dict[race_date][cur_draw] = [records[0], records[1], records[2], records[3], records[4]]
        # after
        for row in rows:
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            horse_code = row['horse_code'].strip()
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    cur_draw = int(sort_history_raceResults_rows[race_date_No][horse_code]['draw'])
                    temp_draw_records[cur_draw][4] += 1
                    if int(cur_plc) == 1:
                        temp_draw_records[cur_draw][0] += 1
                    elif int(cur_plc) == 2:
                        temp_draw_records[cur_draw][1] += 1
                    elif int(cur_plc) == 3:
                        temp_draw_records[cur_draw][2] += 1
                    elif int(cur_plc) == 4:
                        temp_draw_records[cur_draw][3] += 1
    return draw_record_dict

