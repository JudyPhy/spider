import csv
import datetime

words = ['WV', 'WV-A', 'PU', 'WX-A', 'WX', 'UR', 'FE', 'DISQ', 'TNP', 'DNF', '']

HORSE_DEFAULT_SCORE = 1500
JOCKEY_DEFAULT_SCORE = 1500
TRAINER_DEFAULT_SCORE = 1500

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


