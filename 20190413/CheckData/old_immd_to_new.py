from db.db import singleton_ScrubDB
from common import common


def getScrubTableRows(tableName):
    if singleton_ScrubDB.table_exists(tableName):
        singleton_ScrubDB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_ScrubDB.cursor.fetchall()
        singleton_ScrubDB.connect.commit()
        return rows
    print('table[', tableName, '] not exist in scrub')
    return []


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_No INT DEFAULT 0, 
    horse_No INT DEFAULT 0,
    start_time VARCHAR(45) DEFAULT '',
    cls VARCHAR(45) DEFAULT '',
    course VARCHAR(45) DEFAULT '',
    distance INT DEFAULT 0,
    going VARCHAR(45) DEFAULT '',
    exit_race INT DEFAULT 0,
    horse_code VARCHAR(45) DEFAULT '',
    horse_name VARCHAR(45) DEFAULT '',
    draw INT DEFAULT 0,
    wt INT DEFAULT 0,
    jockey VARCHAR(45) DEFAULT '',
    trainer VARCHAR(45) DEFAULT '',
    win_odds VARCHAR(45) DEFAULT '',
    pla_odds VARCHAR(45) DEFAULT '',    
    win_pla VARCHAR(45) DEFAULT '',
    update_time VARCHAR(45) DEFAULT '')'''.format(tableName)
    singleton_ScrubDB.cursor.execute(sql)


def insertToDb(all_list):
    tableName = 'dd_odds_immd_test'
    __createTable(tableName)
    sql = '''insert into {} (race_date,race_No,horse_No,start_time,cls,course,distance,going,exit_race,
    horse_code,horse_name,draw,wt,jockey,trainer,win_odds,pla_odds,win_pla,update_time)
    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(tableName)
    singleton_ScrubDB.cursor.executemany(sql, all_list)
    singleton_ScrubDB.connect.commit()


def main():
    tableName = 'pla_win_odds_2019'
    rows = getScrubTableRows(tableName)
    update_time_rows = {}   # race_date_No & {horse_No & {update_time & row}}
    for row in rows:
        race_date = row['race_date']
        race_No = row['race_no']
        race_date_No = race_date + common.toDoubleDigitStr(race_No)
        if race_date_No not in update_time_rows.keys():
            update_time_rows[race_date_No] = {}
        horse_No = row['horse_no']
        if horse_No not in update_time_rows[race_date_No].keys():
            update_time_rows[race_date_No][horse_No] = {}
        update_time = row['win_update_time']
        if update_time == '':
            update_time = row['pla_update_time']
        update_time = common.toDateTime(update_time)
        update_time_rows[race_date_No][horse_No][update_time] = row

    all_list = []
    for race_date_No, dict_horses in update_time_rows.items():
        for horse_No, dict_rows in dict_horses.items():
            sort_update_time_list = sorted(list(dict_rows.keys()))
            for update_time in sort_update_time_list:
                cur_row = dict_rows[update_time]
                cur_line = (cur_row['race_date'], cur_row['race_no'], cur_row['horse_no'], cur_row['race_time'],
                            cur_row['cls'], cur_row['course'], cur_row['distance'], cur_row['going'],
                            cur_row['exit_race'], cur_row['horse_code'], cur_row['horse_name'], cur_row['draw'],
                            cur_row['wt'], cur_row['jockey'], cur_row['trainer'], cur_row['win_odds'],
                            cur_row['pla_odds'], cur_row['win_pla'], update_time.strftime('%Y-%m-%d %H:%M:%S'))

                all_list.append(cur_line)
    insertToDb(all_list)

main()

