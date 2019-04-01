from db.db import singleton_ScrubDb
from config.myconfig import singleton_cfg
from common import common


def exportRank(race_date, race_id, all_list):
    strs = race_date.split('/')
    tableName = singleton_cfg.getTargetRaceResultsTable(int(strs[2]))
    __createRaceResultsRankTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute("select * from {} where race_date=%s and race_id=%s".format(tableName), (race_date, race_id))
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            pass
            # singleton_ScrubDb.cursor.execute(
            #     '''update {} set plc=%s where race_date=%s and race_id=%s and horse_No=%s and horse_code=%s'''.format(tableName),
            #     (item['plc'], item['race_date'], item['race_id'], item['horse_No'], item['horse_code']))
        else:
            sql_insert = """insert into {}(race_date, race_id, race_No, site, cls, distance, bonus, course, going,
                plc, horse_No, horse, horse_code, jockey, trainer, actual_wt, declar_horse_wt, draw, lbw, running_position, finish_time, win_odds)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tableName)
            singleton_ScrubDb.cursor.executemany(sql_insert, all_list)
        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log('[raceResults]process_RaceResultsRankItem error:' + str(error))


def __createRaceResultsRankTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_id INT DEFAULT 0,
    race_No INT DEFAULT 0,
    site VARCHAR(45) DEFAULT '',
    cls VARCHAR(45) DEFAULT '',
    distance VARCHAR(45) DEFAULT '',
    bonus INT DEFAULT 0,
    course VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',
    plc VARCHAR(45) DEFAULT '',
    horse_No INT DEFAULT 0,
    horse VARCHAR(45) DEFAULT '',
    horse_code VARCHAR(45) DEFAULT '',
    jockey VARCHAR(45) DEFAULT '',
    trainer VARCHAR(45) DEFAULT '',
    actual_wt INT DEFAULT 0,
    declar_horse_wt VARCHAR(45) DEFAULT '',
    draw VARCHAR(45) DEFAULT '',
    lbw VARCHAR(45) DEFAULT '',
    running_position VARCHAR(45) DEFAULT '',
    finish_time VARCHAR(45) DEFAULT '',
    win_odds FLOAT DEFAULT 0.0,
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)


def process_RaceResultsPayoutItem(item):
    strs = item['race_date'].split('/')
    tableName = singleton_cfg.getTargetRacePoolTable(int(strs[2]))
    __createRaceResultsPayTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute(
        """select * from {} where race_date=%s and race_id=%s and pool=%s""".format(tableName),
        (item['race_date'], item['race_id'], item['pool']))
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            pass
        else:
            singleton_ScrubDb.cursor.execute(
            """insert into {}(race_date, race_id, pool, winning_combination, dividend)
            value (%s, %s, %s, %s, %s)""".format(tableName),
            (item['race_date'],
             item['race_id'],
             item['pool'],
             item['winning_combination'],
             item['dividend']))

        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log('[raceResults]process_RaceResultsPayoutItem error:' + str(error))


def __createRaceResultsPayTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_id INT DEFAULT 0,
    pool VARCHAR(45) DEFAULT '',
    winning_combination VARCHAR(45) DEFAULT '',
    dividend VARCHAR(128) DEFAULT '')'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)
