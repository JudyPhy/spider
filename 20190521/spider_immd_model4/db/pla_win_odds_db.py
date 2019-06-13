from db.db import singleton_ScrubDb
import datetime

TARGET_TABLE = 'dd_odds_immd'


def _createTable(tableName):
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
    singleton_ScrubDb.cursor.execute(sql)


def __getLatestOddsRows(race_date, race_No, tableName):
    lastest_odds_rows = {}  # horse_No & row
    if singleton_ScrubDb.table_exists(tableName):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date=%s and race_No=%s'.format(tableName),
                                         (race_date, race_No))
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            horse_No = row['horse_No']
            lastest_odds_rows[horse_No] = row
    else:
        print('table[', tableName, '] not exist')
    return lastest_odds_rows


def __insertSpiderInfo(tableName, race_info, horse_No, wpInfo):
    now = datetime.datetime.now()
    cur_time = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = '''insert into {} (race_date,race_No,horse_No,start_time,cls,course,distance,going,exit_race,
    horse_code,horse_name,draw,wt,jockey,trainer,win_odds,pla_odds,win_pla,update_time)
    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql, (race_info['race_date'], race_info['race_No'], horse_No,
                                           race_info['start_time'], race_info['cls'], race_info['course'],
                                           race_info['distance'], race_info['going'], wpInfo['exit_race'],
                                           wpInfo['horse_code'], wpInfo['horse_name'], wpInfo['draw'],
                                           wpInfo['wt'], wpInfo['jockey'], wpInfo['trainer'], wpInfo['win_odds'],
                                           wpInfo['pla_odds'], wpInfo['win_pla'], cur_time))
    singleton_ScrubDb.connect.commit()


def exportToDb(spider):
    race_date = spider.race_info['race_date']
    race_No = spider.race_info['race_No']
    if race_date == '' or race_No == 0:
        return
    _createTable(TARGET_TABLE)
    lastest_odds_rows = __getLatestOddsRows(race_date, race_No, TARGET_TABLE)
    for horse_No, info in spider.wpTable.items():
        if horse_No in lastest_odds_rows.keys():
            latest_row = lastest_odds_rows[horse_No]
            info_keys = ['cls', 'course', 'distance', 'going']
            for key in info_keys:
                if spider.race_info[key] != latest_row[key]:
                    print('__insertSpiderInfo:', 'key[', key, ']', spider.race_info['race_date'],
                          spider.race_info['race_No'], horse_No, info['horse_code'])
                    __insertSpiderInfo(TARGET_TABLE, spider.race_info, horse_No, info)
                    break
            wp_keys = ['exit_race', 'horse_code', 'horse_name', 'draw', 'wt', 'jockey', 'trainer', 'win_odds', 'pla_odds']
            for key in wp_keys:
                if info[key] != latest_row[key]:
                    print('__insertSpiderInfo:', 'key[', key, ']', spider.race_info['race_date'],
                          spider.race_info['race_No'], horse_No, info['horse_code'])
                    __insertSpiderInfo(TARGET_TABLE, spider.race_info, horse_No, info)
                    break
        else:
            __insertSpiderInfo(TARGET_TABLE, spider.race_info, horse_No, info)

