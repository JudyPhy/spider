from db.db import singleton_ScrubDB
import csv

TABLE_NAME = 't_race_card_20181212'


def getData():
    if singleton_ScrubDB.table_exists(TABLE_NAME):
        singleton_ScrubDB.cursor.execute('select * from {}'.format(TABLE_NAME))
        rows = singleton_ScrubDB.cursor.fetchall()
        singleton_ScrubDB.connect.commit()
        return rows
    return None


def export(allData):
    fileName = TABLE_NAME + '.csv'
    file = open(fileName,  'a+', encoding='utf-8')
    writer = csv.writer(file)
    keys = []
    if len(allData) > 0:
        keys = allData[0].keys()
        print(keys)
    for row in allData:
        writer.writerow(row.values())
    file.close()


def main():
    allData = getData()
    export(allData)

main()