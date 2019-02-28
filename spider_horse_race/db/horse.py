from db.db import singleton_ScrubDb
from config.myconfig import singleton as singleton_cfg
from common import common


def process_HorseInfoItem(item):
    tableName = singleton_cfg.getTargetTable()
    __createHorseInfoTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute(
        """select * from {} where code=%s and name=%s and season=%s and race_id=%s""".format(tableName),
            (item['code'], item['name'], item['season'], item['race_id']))
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            # print(item)
            pass
        else:
            singleton_ScrubDb.cursor.execute(
                """insert into {}(name, code, season, race_id, pla, race_date, rc_track_course, dist, g, class, 
                dr, rtg, trainer, jockey, lbw, win_odds, act_wt, running_position, finish_time, declar_horse_wt,
                gear)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s)""".format(tableName),
                (item['name'],
                 item['code'],
                 item['season'],
                 item['race_id'],
                 item['pla'],
                 item['race_date'],
                 item['rc_track_course'],
                 item['dist'],
                 item['g'],
                 item['class'],
                 item['dr'],
                 item['rtg'],
                 item['trainer'],
                 item['jockey'],
                 item['lbw'],
                 item['win_odds'],
                 item['act_wt'],
                 item['running_position'],
                 item['finish_time'],
                 item['declar_horse_wt'],
                 item['gear']))

        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log('[horse]process_HorseInfoItem error:' + str(error))


def __createHorseInfoTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45) DEFAULT '',
    code VARCHAR(45) DEFAULT '',
    season VARCHAR(45) DEFAULT '',
    race_id VARCHAR(45) DEFAULT '',
    pla VARCHAR(45) DEFAULT '',
    race_date VARCHAR(45) DEFAULT '',
    rc_track_course VARCHAR(45) DEFAULT '',
    dist VARCHAR(45) DEFAULT '',
    g VARCHAR(45) DEFAULT '',
    class VARCHAR(45) DEFAULT '',
    dr VARCHAR(45) DEFAULT '',
    rtg VARCHAR(45) DEFAULT '',
    trainer VARCHAR(45) DEFAULT '',
    jockey VARCHAR(45) DEFAULT '',
    lbw VARCHAR(45) DEFAULT '',
    win_odds VARCHAR(45) DEFAULT '',
    act_wt VARCHAR(45) DEFAULT '',
    running_position VARCHAR(45) DEFAULT '',
    finish_time VARCHAR(45) DEFAULT '',
    declar_horse_wt VARCHAR(45) DEFAULT '',
    gear VARCHAR(45) DEFAULT '',    
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)
