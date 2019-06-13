import csv
import datetime

words = ['WV', 'WV-A', 'PU', 'WX-A', 'WX', 'UR', 'FE', 'DISQ', 'TNP', 'DNF', '']

HORSE_RACE_TABLE = 'c_horse_race_info'

RECE_CARD_TABLE = 't_race_card_{0}'

RESULTS_TABLE = 'f_race_results_{0}'

HORSE_SECTIONAL_TIME_TABLE = 'g_display_sectional_time_{0}'

PEDIGREE_TABLE = 'e_horse_pedigree'

ODDS_SECTIONAL_TABLE = 'h_sectional_odds_{0}'


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

