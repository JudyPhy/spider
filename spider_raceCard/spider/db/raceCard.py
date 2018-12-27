from ..db.db import singleton_ScrubDb
from ..config.myconfig import singleton_cfg
from ..common import common

TAG = 'raceCard'


def process_RaceCardItem(item):
    tableName = singleton_cfg.getTargetRaceCardTable()
    __createRaceCardTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute(
            """select * from {} where race_date=%s and race_No=%s and horse_No=%s""".format(tableName),
            (item['race_date'], item['race_No'], item['horse_No']))
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            pass
        else:
            singleton_ScrubDb.cursor.execute(
                """insert into {}(race_date, race_time, race_id, race_No, site, cls, distance, bonus, course, going,
                horse_No, last_6_runs, horse, horse_code, wt, jockey, over_wt, draw, trainer, rtg, 
                rtg_as, horse_wt_dec, wt_as_dec, best_time, age, wfa, sex, season_stacks, priority, 
                gear, owner, sire, dam, import_cat)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s)""".format(tableName),
                (item['race_date'],
                 item['race_time'],
                 item['race_id'],
                 item['race_No'],
                 item['site'],
                 item['cls'],
                 item['distance'],
                 item['bonus'],
                 item['course'],
                 item['going'],
                 item['horse_No'],
                 item['last_6_runs'],
                 item['horse'],
                 item['horse_code'],
                 item['wt'],
                 item['jockey'],
                 item['over_wt'],
                 item['draw'],
                 item['trainer'],
                 item['rtg'],
                 item['rtg_as'],
                 item['horse_wt_dec'],
                 item['wt_as_dec'],
                 item['best_time'],
                 item['age'],
                 item['wfa'],
                 item['sex'],
                 item['season_stacks'],
                 item['priority'],
                 item['gear'],
                 item['owner'],
                 item['sire'],
                 item['dam'],
                 item['import_cat']))

        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log(TAG + 'process_RaceCardItem error:' + str(error))


def __createRaceCardTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_time VARCHAR(45) DEFAULT '',
    race_id INT DEFAULT 0,
    race_No INT DEFAULT 0,
    site VARCHAR(45) DEFAULT '',
    cls VARCHAR(45) DEFAULT '',
    distance VARCHAR(45) DEFAULT '',
    bonus INT DEFAULT 0,
    course VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',    
    horse_No INT DEFAULT 0,
    last_6_runs VARCHAR(45) DEFAULT '',
    horse VARCHAR(45) DEFAULT '',
    horse_code VARCHAR(45) DEFAULT '',
    wt VARCHAR(45) DEFAULT '',
    jockey VARCHAR(45) DEFAULT '',
    over_wt VARCHAR(45) DEFAULT '',
    draw VARCHAR(45) DEFAULT '',
    trainer VARCHAR(45) DEFAULT '',
    rtg VARCHAR(45) DEFAULT '',
    rtg_as VARCHAR(45) DEFAULT '',
    horse_wt_dec VARCHAR(45) DEFAULT '',
    wt_as_dec VARCHAR(45) DEFAULT '',
    best_time VARCHAR(45) DEFAULT '',
    age INT DEFAULT 0,
    wfa VARCHAR(45) DEFAULT '',
    sex VARCHAR(45) DEFAULT '',
    season_stacks VARCHAR(45) DEFAULT '',
    priority VARCHAR(45) DEFAULT '',
    gear VARCHAR(45) DEFAULT '',
    owner VARCHAR(256) DEFAULT '',
    sire VARCHAR(128) DEFAULT '',
    dam VARCHAR(128) DEFAULT '',
    import_cat VARCHAR(45) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

