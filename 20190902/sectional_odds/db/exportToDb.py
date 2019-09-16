from common import common
from db.database import singleton_Scrub_DB


def __createTable():
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_No INT DEFAULT 0,
    horse_No INT DEFAULT 0,
    before20_odds FLOAT DEFAULT 0,
    before15_odds FLOAT DEFAULT 0,
    before10_odds FLOAT DEFAULT 0,
    before5_odds FLOAT DEFAULT 0)'''.format(common.EXPORT_ODDS_SECTIONAL_TABLE)
    singleton_Scrub_DB.cursor.execute(sql)


def exportToSectionalOddsTable(all_list):
    if singleton_Scrub_DB.table_exists(common.EXPORT_ODDS_SECTIONAL_TABLE):
        singleton_Scrub_DB.cursor.execute('drop table {}'.format(common.EXPORT_ODDS_SECTIONAL_TABLE))
        singleton_Scrub_DB.connect.commit()
    __createTable()
    inster_sql = '''insert into {}(race_date, race_No, horse_No, before20_odds, before15_odds, before10_odds, before5_odds)
    values (%s, %s, %s, %s, %s, %s, %s)'''.format(common.EXPORT_ODDS_SECTIONAL_TABLE)
    singleton_Scrub_DB.cursor.executemany(inster_sql, all_list)
    singleton_Scrub_DB.connect.commit()

