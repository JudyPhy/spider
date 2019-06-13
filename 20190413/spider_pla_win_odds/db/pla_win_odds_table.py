from db.db import singleton_ScrubDb
from common import common
import datetime

TARGET_TABLE = 'pla_win_odds_{0}'


def _createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_no INT DEFAULT 0, 
    horse_no INT DEFAULT 0,
    race_time VARCHAR(45) DEFAULT '',
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
    win_update_time VARCHAR(45) DEFAULT '',
    pla_odds VARCHAR(45) DEFAULT '',
    pla_update_time VARCHAR(45) DEFAULT '',
    win_pla VARCHAR(45) DEFAULT '')'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)


def __toDateTime(time_str):  # time_str: %Y-%m-%d %H:%M:%S
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def __getLatestOddsDict(race_date, race_no, tableName):
    lastest_odds_dict = {}  # race_date_No & {horse_code & [win_odds, win_update_time, pla_odds, pla_update_time, exit_race]}
    if singleton_ScrubDb.table_exists(tableName):
        race_date_No = race_date + common.toDoubleDigitStr(race_no)
        singleton_ScrubDb.cursor.execute('select horse_no,exit_race,win_odds,win_update_time,pla_odds,pla_update_time from {} where race_date=%s and race_no=%s'.format(tableName),
                                         (race_date, race_no))
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            if race_date_No not in lastest_odds_dict.keys():
                lastest_odds_dict[race_date_No] = {}
            horse_no = row['horse_no']
            if horse_no not in lastest_odds_dict[race_date_No].keys():
                lastest_odds_dict[race_date_No][horse_no] = [1, '2000-1-1 00:00:00', 1, '2000-1-1 00:00:00', 0]
            if row['win_update_time'] != '':
                cur_lastest_win_time = __toDateTime(row['win_update_time'])
                prev_lastest_win_time = __toDateTime(lastest_odds_dict[race_date_No][horse_no][1])
                if cur_lastest_win_time > prev_lastest_win_time:
                    lastest_odds_dict[race_date_No][horse_no][0] = row['win_odds']
                    lastest_odds_dict[race_date_No][horse_no][1] = row['win_update_time']
                    lastest_odds_dict[race_date_No][horse_no][4] = row['exit_race']

            if row['pla_update_time'] != '':
                cur_lastest_pla_time = __toDateTime(row['pla_update_time'])
                prev_lastest_pla_time = __toDateTime(lastest_odds_dict[race_date_No][horse_no][3])
                if cur_lastest_pla_time > prev_lastest_pla_time:
                    lastest_odds_dict[race_date_No][horse_no][2] = row['pla_odds']
                    lastest_odds_dict[race_date_No][horse_no][3] = row['pla_update_time']
                    lastest_odds_dict[race_date_No][horse_no][4] = row['exit_race']
    else:
        print('table[', tableName, '] not exist')
    return lastest_odds_dict


def __insertSpiderInfo(tableName, horse_no, raceInfo, wpInfo):
    print('__insertSpiderInfo:', raceInfo['race_date'], raceInfo['race_no'], horse_no, wpInfo['horse_code'])
    sql = '''insert into {} (race_date,race_no,horse_no,race_time,cls,course,distance,going,exit_race,horse_code,
    horse_name,draw,wt,jockey,trainer,win_odds,win_update_time,pla_odds,pla_update_time,win_pla)
    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql, (raceInfo['race_date'], raceInfo['race_no'], horse_no, raceInfo['race_time'], raceInfo['cls'],
                                           raceInfo['course'], raceInfo['distance'], raceInfo['going'], wpInfo['exit_race'], wpInfo['horse_code'],
                                           wpInfo['horse_name'], wpInfo['draw'], wpInfo['wt'], wpInfo['jockey'], wpInfo['trainer'],
                                           wpInfo['win_odds'], wpInfo['win_update_time'], wpInfo['pla_odds'], wpInfo['pla_update_time'], wpInfo['win_pla']))
    singleton_ScrubDb.connect.commit()


def updatePlaOdds(spider):
    print('\nupdateWP raceInfo:', spider.infoDict)
    raceInfo = spider.infoDict
    if raceInfo['race_date'] == '' or raceInfo['race_no'] == 0:
        return
    race_date = raceInfo['race_date']
    race_no = raceInfo['race_no']
    race_date_No = race_date + common.toDoubleDigitStr(race_no)
    tableName = TARGET_TABLE.replace('{0}', race_date[: len(race_date) - 4])
    _createTable(tableName)
    lastest_odds_dict = __getLatestOddsDict(race_date, race_no, tableName)
    for horse_no, info in spider.wpTable.items():
        now = datetime.datetime.now()
        cur_time = now.strftime('%Y-%m-%d %H:%M:%S')
        if (race_date_No in lastest_odds_dict.keys()) and (horse_no in lastest_odds_dict[race_date_No].keys()):
            # compare odds and update table
            lastest_exitRace = lastest_odds_dict[race_date_No][horse_no][4]
            if info['exit_race']:
                if lastest_exitRace != 1:
                    common.log(race_date + str(race_no) + str(horse_no) + ' 退赛')
                    info['horse_code'] = ''
                    info['horse_name'] = ''
                    info['draw'] = 0
                    info['wt'] = 0
                    info['jockey'] = ''
                    info['trainer'] = ''
                    info['win_odds'] = -1
                    info['pla_odds'] = -1
                    info['win_pla'] = -1
                    info['win_update_time'] = cur_time
                    info['pla_update_time'] = cur_time
                    __insertSpiderInfo(tableName, horse_no, raceInfo, info)
            else:
                lastest_win = lastest_odds_dict[race_date_No][horse_no][0]
                lastest_pla = lastest_odds_dict[race_date_No][horse_no][2]
                if (lastest_win != info['win_odds']) and (lastest_pla != info['pla_odds']):
                    info['win_update_time'] = cur_time
                    info['pla_update_time'] = cur_time
                    __insertSpiderInfo(tableName, horse_no, raceInfo, info)
                else:
                    if lastest_win != info['win_odds']:
                        info['win_update_time'] = cur_time
                        info['pla_update_time'] = ''
                        __insertSpiderInfo(tableName, horse_no, raceInfo, info)
                    elif lastest_pla != info['pla_odds']:
                        info['win_update_time'] = ''
                        info['pla_update_time'] = cur_time
                        __insertSpiderInfo(tableName, horse_no, raceInfo, info)
        else:
            # insert odds
            if info['exit_race']:
                info['horse_code'] = ''
                info['horse_name'] = ''
                info['draw'] = 0
                info['wt'] = 0
                info['jockey'] = ''
                info['trainer'] = ''
                info['win_odds'] = -1
                info['pla_odds'] = -1
                info['win_pla'] = -1
            info['win_update_time'] = cur_time
            info['pla_update_time'] = cur_time
            __insertSpiderInfo(tableName, horse_no, raceInfo, info)
    pass

