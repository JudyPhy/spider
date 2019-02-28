from db.db import singleton_ScrubDb
from config.myconfig import singleton as singleton_cfg
from common import common


def process_HorseInfoItem(item):
    tableName = singleton_cfg.getTargetTable()
    __createHorseInfoTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute(
            """select * from {} where code=%s and name=%s""".format(tableName), (item['code'].strip(), item['name']))
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            pass
        else:
            singleton_ScrubDb.cursor.execute(
                """insert into {}(name, code, grow, distance, track_affinity)
                value (%s, %s, %s, %s, %s)""".format(tableName),
                (item['name'],
                 item['code'].strip(),
                 item['grow'],
                 item['distance'],
                 item['track_affinity']))

        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log('[horse]process_HorseInfoItem error:' + str(error))


def __createHorseInfoTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45) DEFAULT '',
    code VARCHAR(45) DEFAULT '',
    grow VARCHAR(128) DEFAULT '',
    distance VARCHAR(128) DEFAULT '',
    track_affinity VARCHAR(128) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

