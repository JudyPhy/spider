from common import common


def __getImmdGoing(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        return immd_info_dict[race_date_No][horse_No]['going']
    return ''


# future_raceCard_rows: race_date_No & {horse_No & row}
# immd_info_dict: race_date_No & {horse_No & row}
def __getTodayGoingDict(future_raceCard_rows, immd_info_dict):
    going_dict = {}  # race_date_No & going
    going_type = []
    for race_date_No, horse_dict in future_raceCard_rows.items():
        for horse_code, row in horse_dict.items():
            if race_date_No not in going_dict.keys():
                horse_No = row['horse_No']
                going = __getImmdGoing(race_date_No, horse_No, immd_info_dict)
                if going == '':
                    going = row['going']
                going = going.replace(' ', '').upper()
                if going == '':
                    going = 'GOOD'
                going_dict[race_date_No] = going

                # log
                if going not in going_type:
                    going_type.append(going)
    print('today going_type:', going_type)
    return going_dict


# race_results_rows: race_date_No & {horse_code & row}
def __getHistoryGoingDict(historay_raceResults_rows):
    going_dict = {}  # race_date_No & going
    for race_date_No, horse_dict in historay_raceResults_rows.items():
        for horse_code, row in horse_dict.items():
            if race_date_No not in going_dict.keys():
                going = row['going'].replace(' ', '').upper()
                if going == '':
                    going = 'GOOD'
                going_dict[race_date_No] = going
    return going_dict


def GetAllGoingDict(future_raceCard_rows, immd_info_dict, historay_raceResults_rows):
    today_going_dict = __getTodayGoingDict(future_raceCard_rows, immd_info_dict)
    history_going_dict = __getHistoryGoingDict(historay_raceResults_rows)
    going_dict = {}   # race_date_No & going
    going_dict.update(history_going_dict)
    going_dict.update(today_going_dict)

    # check log
    sum_count = len(today_going_dict) + len(history_going_dict)
    combine_count = len(going_dict)
    if sum_count != combine_count:
        print('error: going[', sum_count, ', ', combine_count, ']')

    return going_dict

