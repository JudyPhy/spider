from db.db import singleton_ScrubDb
from url.horse_race_url import HorseRaceUrl
from common import common


def exportToDb(horse_info, horse_race_dict):
    tableName = HorseRaceUrl().EXPORT_TABLE
    __createTable(tableName)
    all_list = []
    for season, array in horse_race_dict.items():
        for dict in array:
            try:
                singleton_ScrubDb.cursor.execute(
                """select * from {} where code=%s and name=%s and season=%s and race_id=%s""".format(tableName),
                    (horse_info['code'], horse_info['name'], season, dict['race_id']))
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
                        (horse_info['name'],
                         horse_info['code'],
                         season,
                         dict['race_id'],
                         dict['pla'],
                         dict['race_date'],
                         dict['rc_track_course'],
                         dict['dist'],
                         dict['g'],
                         dict['class'],
                         dict['dr'],
                         dict['rtg'],
                         dict['trainer'],
                         dict['jockey'],
                         dict['lbw'],
                         dict['win_odds'],
                         dict['act_wt'],
                         dict['running_position'],
                         dict['finish_time'],
                         dict['declar_horse_wt'],
                         dict['gear']))
                singleton_ScrubDb.connect.commit()
            except Exception as error:
                common.log('horse race export to db error:' + str(error))


def __createTable(tableName):
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



