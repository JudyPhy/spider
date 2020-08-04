from db.db import singleton_ScrubDb
from common import common
from url.race_card_url import RaceCardSpiderUrl


def exportToHistoryDb(race_info, race_card_table):
    if len(race_card_table) <= 0:
        return
    tableName = RaceCardSpiderUrl().HISTORY_EXPORT_TABLE
    __createTable(tableName)
    for row in race_card_table:
        try:
            singleton_ScrubDb.cursor.execute("select * from {} where race_date=%s and race_No=%s and horse_No=%s and horse_code=%s".format(tableName),
                                             (race_info['race_date'], race_info['race_No'], row[0], row[4]))
            repetition = singleton_ScrubDb.cursor.fetchone()
            if repetition:
                # sql_update = """update {} set going=%s, distance=%s, course=%s, cls=%s, bonus=%s
                # where race_date=%s and race_No=%s and horse_No=%s and horse_code=%s""".format(tableName)
                # cur_list = [race_info['going'], race_info['distance'], race_info['course'], race_info['cls'], race_info['bonus']]
                # cur_list += [race_info['race_date'], race_info['race_No'], row[0], row[2]]
                # singleton_ScrubDb.cursor.execute(sql_update, (cur_list))
                pass
            else:
                sql_insert = """insert into {}(race_No, race_date, site, race_time, course, going, distance, cls, bonus, race_id, 
                horse_No, last_6_runs, color, horse, horse_code, wt, jockey, over_wt, draw, trainer, 
                rtg, rtg_as, horse_wt_dec, wt_as_dec, best_time, age, wfa, sex, season_stacks, priority, 
                gear, owner, sire, dam, import_cat)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s)""".format(tableName)
                cur_list = list(race_info.values())
                cur_list.append(0)
                cur_list += row
                singleton_ScrubDb.cursor.execute(sql_insert, (cur_list))
        except Exception as error:
            common.log('history race card export to db error:' + str(error))
    singleton_ScrubDb.connect.commit()


def exportToFutureDb(race_info, race_card_table):
    if len(race_card_table) <= 0:
        return
    tableName = RaceCardSpiderUrl().FUTURE_EXPORT_TABLE
    __createTable(tableName)
    for row in race_card_table:
        try:
            singleton_ScrubDb.cursor.execute("select * from {} where race_date=%s and race_No=%s and horse_No=%s".format(tableName),
                                             (race_info['race_date'], race_info['race_No'], row[0]))
            repetition = singleton_ScrubDb.cursor.fetchone()
            if repetition:
                sql_update = """update {} set site=%s, race_time=%s, going=%s, distance=%s, course=%s, 
                cls=%s, bonus=%s, last_6_runs=%s, color=%s, horse=%s, horse_code=%s, wt=%s, jockey=%s, 
                over_wt=%s, draw=%s, trainer=%s, rtg=%s, rtg_as=%s, horse_wt_dec=%s, wt_as_dec=%s, best_time=%s, 
                age=%s, wfa=%s, sex=%s, season_stacks=%s, priority=%s, gear=%s, owner=%s, sire=%s, 
                dam=%s, import_cat=%s where race_date=%s and race_No=%s and horse_No=%s""".format(tableName)
                cur_list = [race_info['site'], race_info['startTime'], race_info['going'], race_info['distance'], race_info['course'],
                            race_info['cls'], race_info['bonus']]
                cur_list += row[1:]
                cur_list += [race_info['race_date'], race_info['race_No'], row[0]]
                singleton_ScrubDb.cursor.execute(sql_update, (cur_list))
            else:
                sql_insert = """insert into {}(race_No, race_date, site, race_time, course, going, distance, cls, bonus, race_id, 
                horse_No, last_6_runs, color, horse, horse_code, wt, jockey, over_wt, draw, trainer, 
                rtg, rtg_as, horse_wt_dec, wt_as_dec, best_time, age, wfa, sex, season_stacks, priority, 
                gear, owner, sire, dam, import_cat)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s)""".format(tableName)
                cur_list = list(race_info.values())
                cur_list.append(0)
                cur_list += row
                singleton_ScrubDb.cursor.execute(sql_insert, (cur_list))
        except Exception as error:
            common.log('future race card export to db error:' + str(error))
    singleton_ScrubDb.connect.commit()


def __createTable(tableName):
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
    horse_No VARCHAR(45) DEFAULT '',
    last_6_runs VARCHAR(45) DEFAULT '',
    color VARCHAR(45) DEFAULT '',
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
    age VARCHAR(45) DEFAULT '',
    wfa VARCHAR(45) DEFAULT '',
    sex VARCHAR(45) DEFAULT '',
    season_stacks VARCHAR(45) DEFAULT '',
    priority VARCHAR(45) DEFAULT '',
    gear VARCHAR(45) DEFAULT '',
    owner VARCHAR(1024) DEFAULT '',
    sire VARCHAR(128) DEFAULT '',
    dam VARCHAR(128) DEFAULT '',
    import_cat VARCHAR(45) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

