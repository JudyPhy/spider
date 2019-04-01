from db.db import singleton_ScrubDb
from config.myconfig import singleton_cfg


def _createTable(tableName):
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


def export(race_date, race_No, all_rows):
    year = race_date[: len(race_date) - 4]
    tableName = singleton_cfg.getTargetTable().replace('{0}', year)
    _createTable(tableName)
    singleton_ScrubDb.cursor.execute('select id from {} where race_date=%s and race_No=%s'.format(tableName), (race_date, race_No))
    row = singleton_ScrubDb.cursor.fetchone()
    if row:
        pass
    else:
        sql = '''insert into {} (race_date, race_No, horse_No, section1, section2, section3, section4, draw,
        odds1, odds2, odds3, odds4)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s)'''.format(tableName)
        singleton_ScrubDb.cursor.executemany(sql, all_rows)
    singleton_ScrubDb.connect.commit()


