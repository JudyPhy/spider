from db.db import singleton_ScrubDb
from url.horse_pedigree_url import HorsePedigreeUrl
from common import common


def exportToDb(horse_info):
    if (horse_info == {}) or \
            (('grow' not in horse_info.keys()) and ('distance' not in horse_info.keys()) and ('track_affinity' not in horse_info.keys())):
        return
    tableName = HorsePedigreeUrl().EXPORT_TABLE
    __createTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute(
            """select * from {} where code=%s and name=%s""".format(tableName),
            (horse_info['code'].strip(), horse_info['name']))
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            pass
        else:
            singleton_ScrubDb.cursor.execute(
                """insert into {}(name, code, grow, distance, track_affinity)
                value (%s, %s, %s, %s, %s)""".format(tableName),
                (horse_info['name'],
                 horse_info['code'].strip(),
                 horse_info['grow'],
                 horse_info['distance'],
                 horse_info['track_affinity']))
        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log('horse pedigree export to db error:' + str(error))


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45) DEFAULT '',
    code VARCHAR(45) DEFAULT '',
    grow VARCHAR(128) DEFAULT '',
    distance VARCHAR(128) DEFAULT '',
    track_affinity VARCHAR(128) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

