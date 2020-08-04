from db.db import singleton_ScrubDb
from common import common
from url.sectional_odds_url import SectionalOddsUrl


def exportToDb(race_date, race_No, sectionalTime, oddsDict):
    if len(oddsDict) <= 0:
        return
    tableName = SectionalOddsUrl().EXPORT_TABLE
    __createTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute('select id from {} where race_date=%s and race_No=%s'.format(tableName),
                                         (race_date, race_No))
        row = singleton_ScrubDb.cursor.fetchone()
        if row:
            pass
        else:
            all_rows = []
            for horse_No, cur_row in oddsDict.items():
                cur_list = [race_date, race_No, horse_No]
                cur_list += sectionalTime
                cur_list += cur_row[1:]
                cur_list = (cur_list)
                all_rows.append(cur_list)
            sql = '''insert into {} (race_date, race_No, horse_No, section1, section2, section3, section4,
            draw, odds1, odds2, odds3, odds4) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(tableName)
            singleton_ScrubDb.cursor.executemany(sql, all_rows)
    except Exception as error:
        common.log('sectional odds export to db error:' + str(error))
    singleton_ScrubDb.connect.commit()


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_No INT DEFAULT 0, 
    horse_No INT DEFAULT 0,
    section1 VARCHAR(45) DEFAULT '',
    section2 VARCHAR(45) DEFAULT '',
    section3 VARCHAR(45) DEFAULT '',
    section4 VARCHAR(45) DEFAULT '',
    draw INT DEFAULT 0,
    odds1 VARCHAR(45) DEFAULT '',
    odds2 VARCHAR(45) DEFAULT '',
    odds3 VARCHAR(45) DEFAULT '',
    odds4 VARCHAR(45) DEFAULT '')ENGINE=InnoDB DEFAULT CHARSET=utf8'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

