import csv
import datetime
from db.database import singleton_Scrub_DB

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

def log(msg):
    print(msg)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file = open('log.csv', 'a+', newline='')
    writer = csv.writer(file)
    writer.writerow([msg, now])
    file.close()

FUTURE_HORSE_INFO_TABLE = 'a_future_horse_info_{0}'


def getFutureHorseTableList():
    tableList = []
    now = datetime.datetime.now()
    for year in range(now.year, 2017, -1):
        # tableList.append('a_future_horse_info_B_20181219')
        tableList.append(FUTURE_HORSE_INFO_TABLE.replace('{0}', str(year)))
    return tableList

def getHistoryHorseTableList():
    tableList = []
    now = datetime.datetime.now()
    for year in range(now.year, 2012, -1):
        for month in range(12, 0, -1):
            for day in range(31, 0, -1):
                str_date = str(year) + toDoubleDigitStr(month) + toDoubleDigitStr(day)
                tableName = 'a_all_horse_info_' + str_date
                if singleton_Scrub_DB.table_exists(tableName):
                    tableList.append(tableName)
    return tableList

