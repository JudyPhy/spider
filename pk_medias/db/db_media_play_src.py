from db.db import singleton_PKMediaDb
from common import common


def exportToDb(type, result):
    print('exportToDb: url->', type, result)
    tableName = common.MEDIA_PLAY_SRC_TABLE + '_' + type
    __createTable(tableName)
    try:
        singleton_PKMediaDb.cursor.execute("select * from {} where data_id=%s".format(tableName), result[0])
        repetition = singleton_PKMediaDb.cursor.fetchone()
        if not repetition:
            sql_insert = """insert into {}(data_id, url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11) 
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tableName)
            singleton_PKMediaDb.cursor.execute(sql_insert, (result))
        else:
            sql_update = """update {} set url1=%s, url2=%s, url3=%s, url4=%s, url5=%s, url6=%s, url7=%s, url8=%s, 
            url9=%s, url10=%s, url11=%s where data_id=%s""".format(tableName)
            params = result[1:].append(result[0])
            singleton_PKMediaDb.cursor.execute(sql_update, (params))
        singleton_PKMediaDb.connect.commit()
    except Exception as error:
        common.log('media play src export to db error:' + str(error))


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_id VARCHAR(45) DEFAULT '',
    url1 TEXT,
    url2 TEXT,
    url3 TEXT,
    url4 TEXT,
    url5 TEXT,
    url6 TEXT,
    url7 TEXT,
    url8 TEXT,
    url9 TEXT,
    url10 TEXT,
    url11 TEXT,
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_PKMediaDb.cursor.execute(sql)

