from db.db import singleton_ScrubDb
from config.myconfig import singleton_cfg


def exportToDb(race_date, all_list):
    tableName = singleton_cfg.getTargetExportTable()
    __createTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute("select * from {} where race_date=%s".format(tableName), race_date)
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            pass
        else:
            sql_insert = """insert into {}(race_date, race_No, race_id, pool, winning_combination, dividend)
            values (%s, %s, %s, %s, %s, %s)""".format(tableName)
            singleton_ScrubDb.cursor.executemany(sql_insert, all_list)
        singleton_ScrubDb.connect.commit()
    except Exception as error:
        print('exportToDb error:' + str(error))


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_No INT DEFAULT 0,
    race_id INT DEFAULT 0,
    pool VARCHAR(45) DEFAULT '',
    winning_combination VARCHAR(45) DEFAULT '',
    dividend VARCHAR(128) DEFAULT '')'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)
