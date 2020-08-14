from db.db import singleton_PKMediaDb
from common import common


def exportToDb(type, result):
    print('exportToDb: meta->', type, result)
    tableName = common.MEDIA_META_TABLE + '_' + type
    __createTable(tableName)
    try:
        singleton_PKMediaDb.cursor.execute("select * from {} where data_id=%s".format(tableName), result[0])
        repetition = singleton_PKMediaDb.cursor.fetchone()
        if not repetition:
            sql_insert = """insert into {}(data_id, cover, title, director, screenwriter, starring, type, area, 
            language, releaseTime, length, other_name, score, introduce) 
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tableName)
            singleton_PKMediaDb.cursor.execute(sql_insert, (result))
        # else:
        #     sql_update = """update {} set cover=%s, title=%s, director=%s, screenwriter=%s, starring=%s, type=%s,
        #     area=%s, language=%s, releaseTime=%s, length=%s other_name=%s, score=%s, introduce=%s where data_id=%s""".format(tableName)
        #     params = result[1:].append(result[0])
        #     singleton_PKMediaDb.cursor.execute(sql_update, (params))
        singleton_PKMediaDb.connect.commit()
    except Exception as error:
        common.log('media play src export to db error:' + str(error))


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_id VARCHAR(45) DEFAULT '',
    cover TEXT,
    title VARCHAR(128) DEFAULT '',
    director VARCHAR(128) DEFAULT '',
    screenwriter VARCHAR(128) DEFAULT '',
    starring TEXT,
    type VARCHAR(45) DEFAULT '',
    area VARCHAR(45) DEFAULT '',
    language VARCHAR(128) DEFAULT '',
    releaseTime VARCHAR(128) DEFAULT '',
    length VARCHAR(128) DEFAULT '',
    other_name VARCHAR(128) DEFAULT '',
    score VARCHAR(128) DEFAULT '',
    introduce TEXT,
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_PKMediaDb.cursor.execute(sql)

