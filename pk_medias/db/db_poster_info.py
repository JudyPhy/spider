from db.db import singleton_PKMediaDb
from common import common


def exportToDb(result, type):
    tableName = common.POSTER_INFO_TABLE + '_' + type
    __createTable(tableName)
    try:
        singleton_PKMediaDb.cursor.execute("select id from {} where data_id=%s".format(tableName), result[0])
        repetition = singleton_PKMediaDb.cursor.fetchone()
        if not repetition:
            sql_insert = """insert into {}(data_id, detail_url, title, img_src, score, tag) value 
            (%s, %s, %s, %s, %s, %s)""".format(tableName)
            singleton_PKMediaDb.cursor.execute(sql_insert, (result))
    except Exception as error:
        common.log('poster info export to db error:' + str(error))
    singleton_PKMediaDb.connect.commit()


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_id VARCHAR(45) DEFAULT '',
    detail_url TEXT,
    title VARCHAR(45) DEFAULT '',
    img_src TEXT,
    score VARCHAR(45) DEFAULT '',
    tag VARCHAR(45) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_PKMediaDb.cursor.execute(sql)

