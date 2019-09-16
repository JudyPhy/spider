from common import common


def __getCorseRecords(horse_code, course, history_raceResults_rows):
    course_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
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


def GetHorseCourseRecord(future_raceCard_rows, history_raceResults_rows):
    course_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in course_record_dict.keys():
            course_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            course = row['course'].strip().upper()
            if '"' in course:
                array_course = course.split('"')
                course = array_course[1].strip()
            course_record_dict[race_date_No][horse_No] = __getCorseRecords(horse_code, course, history_raceResults_rows)
    return course_record_dict

