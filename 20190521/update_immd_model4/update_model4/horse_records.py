from common import common

RECENT_COUNT = 6


def getRecords(horse_code, race_results_rows):
    rescords = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                rescords[4] += 1
                if int(plc) == 1:
                    rescords[0] += 1
                elif int(plc) == 2:
                    rescords[1] += 1
                elif int(plc) == 3:
                    rescords[2] += 1
                elif int(plc) == 4:
                    rescords[3] += 1
    return rescords


def getRecentRecord(horse_code, race_results_rows):
    records = [0, 0, 0, 0, 0]
    sort_date_No_list = sorted(race_results_rows.keys())
    sort_date_No_list.reverse()
    count = 0
    for race_date_No in sort_date_No_list:
        dict = race_results_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                records[4] += 1
                if int(plc) == 1:
                    records[0] += 1
                elif int(plc) == 2:
                    records[1] += 1
                elif int(plc) == 3:
                    records[2] += 1
                elif int(plc) == 4:
                    records[3] += 1
                count += 1
                if count >= RECENT_COUNT:
                    break
    return records


def getSiteRecord(horse_code, site, race_results_rows):
    site_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_site = dict[horse_code]['site'].replace(' ', '')
            if (plc not in common.words) and (site == cur_site):
                site_records[4] += 1
                if int(plc) == 1:
                    site_records[0] += 1
                elif int(plc) == 2:
                    site_records[1] += 1
                elif int(plc) == 3:
                    site_records[2] += 1
                elif int(plc) == 4:
                    site_records[3] += 1
    return site_records


def getGoingRecords(horse_code, going, race_results_rows):
    going_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_going = dict[horse_code]['going'].replace(' ', '').upper()
            if cur_going == '':
                cur_going = 'GOOD'
            if (plc not in common.words) and (cur_going == going):
                going_records[4] += 1
                if int(plc) == 1:
                    going_records[0] += 1
                elif int(plc) == 2:
                    going_records[1] += 1
                elif int(plc) == 3:
                    going_records[2] += 1
                elif int(plc) == 4:
                    going_records[3] += 1
    return going_records


def getCorseRecords(horse_code, course, race_results_rows):
    course_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_course = dict[horse_code]['course'].strip().upper()
            if '"' in cur_course:
                array_course = cur_course.split('"')
                cur_course = array_course[1].strip()
            if (plc not in common.words) and (cur_course == course):
                course_records[4] += 1
                if int(plc) == 1:
                    course_records[0] += 1
                elif int(plc) == 2:
                    course_records[1] += 1
                elif int(plc) == 3:
                    course_records[2] += 1
                elif int(plc) == 4:
                    course_records[3] += 1
    return course_records


def getDistanceRecords(horse_code, distance, race_results_rows):
    distance_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_distance = int(dict[horse_code]['distance'])
            if (plc not in common.words) and (cur_distance == distance):
                distance_records[4] += 1
                if int(plc) == 1:
                    distance_records[0] += 1
                elif int(plc) == 2:
                    distance_records[1] += 1
                elif int(plc) == 3:
                    distance_records[2] += 1
                elif int(plc) == 4:
                    distance_records[3] += 1
    return distance_records


def getClassRecords(horse_code, cls, race_results_rows):
    cls_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_cls = dict[horse_code]['cls'].replace('Class', '').strip()
            if (plc not in common.words) and (cur_cls == cls):
                cls_records[4] += 1
                if int(plc) == 1:
                    cls_records[0] += 1
                elif int(plc) == 2:
                    cls_records[1] += 1
                elif int(plc) == 3:
                    cls_records[2] += 1
                elif int(plc) == 4:
                    cls_records[3] += 1
    return cls_records


def getDrawRecord(horse_code, draw, race_results_rows):
    draw_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
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


def getJockeyRecord(horse_code, jockey, race_results_rows):
    jockey_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            array_jockey = dict[horse_code]['jockey'].split('(')
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

