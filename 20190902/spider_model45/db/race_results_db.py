from db.db import singleton_ScrubDb
from common import common
from url.race_results_url import RaceResultsUrl


def exportToDb(race_info, rank_table):
    if len(rank_table) <= 0:
        return
    tableName = RaceResultsUrl().EXPORT_TABLE
    __createTable(tableName)
    for row in rank_table:
        try:
            singleton_ScrubDb.cursor.execute("select * from {} where race_date=%s and race_No=%s and horse_No=%s and horse_code=%s".format(tableName),
                                             (race_info['race_date'], race_info['race_No'], row[1], row[3]))
            repetition = singleton_ScrubDb.cursor.fetchone()
            if repetition:
                pass
            else:
                sql_insert = """insert into {}(race_date, site, race_id, race_No, cls, distance, going, bonus, course,
                    plc, horse_No, horse, horse_code, jockey, trainer, actual_wt, declar_horse_wt, draw, lbw, running_position, finish_time, win_odds)
                    value (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tableName)
                cur_list = list(race_info.values())
                cur_list += row
                singleton_ScrubDb.cursor.execute(sql_insert, (cur_list))
        except Exception as error:
            common.log('race results export to db error:' + str(error))
    singleton_ScrubDb.connect.commit()


def __createTable(tableName):
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
    horse_No VARCHAR(45) DEFAULT '',
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

