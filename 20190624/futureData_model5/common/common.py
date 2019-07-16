import csv
import datetime

words = ['WV', 'WV-A', 'PU', 'WX-A', 'WX', 'UR', 'FE', 'DISQ', 'TNP', 'DNF', '', 'WXNR']

HORSE_RACE_TABLE = 'cc_horse_race_info'

PEDIGREE_TABLE = 'ee_horse_pedigree'

RECE_CARD_TABLE = 'tt_race_card_history'

FUTURE_RECE_CARD_TABLE = 'tt_race_card_future'

RESULTS_TABLE = 'ff_race_results'

HORSE_SECTIONAL_TIME_TABLE = 'gg_display_sectional_time'

ODDS_TABLE = 'pla_win_odds_{0}'

COURSE_STANDARD_TIMES_TABLE = 'ii_course_standard_times'

def toDoubleDigitStr(interger):
    v_char = str(interger)
    while len(v_char) < 2:
        v_char = '0' + v_char
    return v_char


def toThreeDigitStr(interger):
    v_char = str(interger)
    while len(v_char) < 3:
        v_char = '0' + v_char
    return v_char


def toIntDate(str_date, split_flag):
    array = str_date.split(split_flag)
    return int(array[0]), int(array[1]), int(array[2])


def log(msg):
    print(msg)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file = open('log.csv', 'a+', newline='')
    writer = csv.writer(file)
    writer.writerow([msg, now])
    file.close()


def __toHorseRaceClass(cls):
    if cls in ['1', '2', '3', '4', '5']:
        return cls
    elif 'Hong Kong Group One' == cls:
        return 'HKG1'
    elif 'Hong Kong Group Two' == cls:
        return 'HKG2'
    elif 'Hong Kong Group Three' == cls:
        return 'HKG3'
    elif 'Group One' == cls:
        return 'G1'
    elif 'Group Two' == cls:
        return 'G2'
    elif 'Group Three' == cls:
        return 'G3'
    elif '4 Year Olds' == cls:
        return '4YO'
    elif '4 (Restricted)' == cls:
        return '4R'
    elif '4 (Special Condition)' == cls:
        return '4S'
    elif '3 (Special Condition)' == cls:
        return '3S'
    elif 'Restricted Race' == cls:
        return 'R'
    elif 'Griffin Race' == cls:
        return 'GRIFFIN'
    else:
        return None


def GetTotalSeconds(time_text):
    seconds = 0
    array_time = []
    array1 = time_text.split('.')
    for item1 in array1:
        array2 = item1.split(':')
        for item2 in array2:
            array_time.append(item2)
    if len(array_time) == 3:
        seconds = int(array_time[0]) * 60 + int(array_time[1]) + int(array_time[2]) / 100
    elif len(array_time) == 2:
        seconds = int(array_time[0]) + int(array_time[1]) / 100
    elif len(array_time) == 1:
        seconds = int(array_time[0]) / 100
    return seconds


def IsLowestOdds(odds, rows):
    for horse_code, row in rows.items():
        cur_odds = float(row['win_odds'])
        if cur_odds < odds:
            return False
    return True


def GetSameTrainerCount(trainer, rows):
    count = 0
    for horse_code, row in rows.items():
        array_trainer = row['trainer'].split('(')
        cur_trainer = array_trainer[0].strip()
        if cur_trainer == trainer:
            count += 1
    return count


def GetBeforeNDayDate(today, deltaDays):
    detaday = datetime.timedelta(days=deltaDays)
    target_date = today - detaday
    race_date = str(target_date.year) + toDoubleDigitStr(target_date.month) + toDoubleDigitStr(target_date.day)
    return race_date


