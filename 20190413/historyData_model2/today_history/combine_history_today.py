### 合并原始数据，存储到export_table表中 ###
from db.database import singleton_Results_DB
from common import common

EXPORT_TABLE = 'table_test_odds'

HISTORY_TABLE = 'table_dragon_20130101_20181205'

def __getSourceData(tableName):
    all = []
    if singleton_Results_DB.table_exists(tableName):
        singleton_Results_DB.cursor.execute("select * from {}".format(tableName))
        all = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in all:
            array_course = row['course'].split('"')
            if len(array_course) == 3:
                row['course'] = array_course[1]
            row['site'] = row['site'].replace(' ', '')
    else:
        common.log('Table[' + tableName + '] not exist.')
    return all


def __createTable():
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date INT DEFAULT 0,
    raceDays INT DEFAULT 0,
    race_id BIGINT DEFAULT 0,
    horse_no INT DEFAULT 0,
    pla_odds FLOAT DEFAULT 0.0,
    win_odds FLOAT DEFAULT 0.0,
    score INT DEFAULT 0,
    plc INT DEFAULT 0,
    declar_horse_wt INT DEFAULT 0,
    current_rating INT DEFAULT 0,
    total_stakes INT DEFAULT 0,
    count INT DEFAULT 0,
    race_no INT DEFAULT 0,
    cls VARCHAR(45) DEFAULT '',
    distance INT DEFAULT 0,
    bonus INT DEFAULT 0,
    actual_wt INT DEFAULT 0,
    draw INT DEFAULT 0,
    season_stakes INT DEFAULT 0,
    horse_age INT DEFAULT 0,
    horse_star_0_curRace INT DEFAULT 0,
    horse_star_1_curRace INT DEFAULT 0,
    horse_star_2_curRace INT DEFAULT 0,
    horse_star_3_curRace INT DEFAULT 0,
    horse_total_curRace INT DEFAULT 0,
    horse_star_0_allRace INT DEFAULT 0,
    horse_star_1_allRace INT DEFAULT 0,
    horse_star_2_allRace INT DEFAULT 0,
    horse_star_3_allRace INT DEFAULT 0,
    horse_total_allRace INT DEFAULT 0,
    site VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',
    course VARCHAR(45) DEFAULT '',
    pre_race_speed FLOAT DEFAULT 0,
    race_speed FLOAT DEFAULT 0)'''.format(EXPORT_TABLE)
    singleton_Results_DB.cursor.execute(sql)


def getTodayHistoryWinOddsDict(rows):
    results_list = []   # [{race_no, horse_no, win_odds}, {race_no, horse_no, win_odds}, ...]
    for row in rows:
        if row['race_date'] == 20181205:
            item = {}
            item['race_no'] = row['race_no']
            item['horse_no'] = row['horse_no']
            item['win_odds'] = row['win_odds']
            results_list.append(item)
    return results_list


def getTodayHistoryWinOdds(row, win_odds_dict):
    for item in win_odds_dict:
        if item['race_no'] == row['race_no'] and item['horse_no'] == row['horse_no']:
            return item['win_odds']
    print("history data doesn't contain win_odds in today data")
    return row['win_odds']


def getTodayHistoryPlcDict(rows):
    results_list = []  # [{race_no, horse_no, plc}, {race_no, horse_no, plc}, ...]
    for row in rows:
        if row['race_date'] == 20181205:
            item = {}
            item['race_no'] = row['race_no']
            item['horse_no'] = row['horse_no']
            item['plc'] = row['plc']
            results_list.append(item)
    return results_list


def getTodayHistoryPlc(row, plc_dict):
    for item in plc_dict:
        if item['race_no'] == row['race_no'] and item['horse_no'] == row['horse_no']:
            return item['plc']
    print("history data doesn't contain plc in today data")
    return row['plc']


def updateTodayPlc():
    singleton_Results_DB.cursor.execute('select race_date,race_no,horse_no,plc from {}'.format(HISTORY_TABLE))
    rows = singleton_Results_DB.cursor.fetchall()
    plc_dict = getTodayHistoryPlcDict(rows)

    singleton_Results_DB.cursor.execute('select race_date,race_no,horse_no from {}'.format(EXPORT_TABLE))
    rows = singleton_Results_DB.cursor.fetchall()
    for row in rows:
        if row['race_date'] == 20181205:
            plc = getTodayHistoryPlc(row, plc_dict)
            sql = '''update {} set plc=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(EXPORT_TABLE)
            singleton_Results_DB.cursor.execute(sql, (plc, row['race_date'], row['race_no'], row['horse_no']))
    singleton_Results_DB.connect.commit()


def updateTodayWinOdds():
    singleton_Results_DB.cursor.execute('select race_date,race_no,horse_no,win_odds from {}'.format(HISTORY_TABLE))
    rows = singleton_Results_DB.cursor.fetchall()
    win_odds_dict = getTodayHistoryWinOddsDict(rows)

    singleton_Results_DB.cursor.execute('select race_date,race_no,horse_no from {}'.format(EXPORT_TABLE))
    rows = singleton_Results_DB.cursor.fetchall()
    for row in rows:
        if row['race_date'] == 20181205:
            win_odds = getTodayHistoryWinOdds(row, win_odds_dict)
            sql = '''update {} set win_odds=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(EXPORT_TABLE)
            singleton_Results_DB.cursor.execute(sql, (win_odds, row['race_date'], row['race_no'], row['horse_no']))
    singleton_Results_DB.connect.commit()


def updateTodayGoing():
    singleton_Results_DB.cursor.execute('select race_date,race_no,horse_no,site,going,course from {}'.format(HISTORY_TABLE))
    rows_orig = singleton_Results_DB.cursor.fetchall()
    singleton_Results_DB.connect.commit()
    for row in rows_orig:
        race_date = row['race_date']
        if race_date == 20181205:
            race_no = row['race_no']
            horse_no = row['horse_no']
            sql = 'update {} set going=%s where race_date=%s and race_no=%s and horse_no=%s'.format(EXPORT_TABLE)
            singleton_Results_DB.cursor.execute(sql, (row['going'], race_date, race_no, horse_no))
            singleton_Results_DB.connect.commit()


def main():
    if singleton_Results_DB.table_exists(EXPORT_TABLE):
        singleton_Results_DB.cursor.execute('drop table {}'.format(EXPORT_TABLE))
        singleton_Results_DB.connect.commit()
    __createTable()
    sql = '''insert into {}(race_date, raceDays, race_id, horse_no, pla_odds, win_odds, score, plc,
    declar_horse_wt, current_rating, total_stakes, count, race_no, cls, distance, bonus, actual_wt,
    draw, season_stakes, horse_age,
    horse_star_0_curRace, horse_star_1_curRace, horse_star_2_curRace, horse_star_3_curRace, horse_total_curRace,
    horse_star_0_allRace, horse_star_1_allRace, horse_star_2_allRace, horse_star_3_allRace, horse_total_allRace,
    site, going, course, pre_race_speed, race_speed)
    values (%s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s)'''.format(EXPORT_TABLE)

    items_list = []
    for table in ['today_table_dragon_20181205', 'table_dragon_20130101_20181203']:
        source_list = __getSourceData(table)
        for row in source_list:
            row_list = list(row.values())[1:]
            cur_row_list = (row_list)
            # print(cur_row_list)
            items_list.append(cur_row_list)
    singleton_Results_DB.cursor.executemany(sql, items_list)
    singleton_Results_DB.connect.commit()

    updateTodayWinOdds()
    # updateTodayPlc()
    updateTodayGoing()