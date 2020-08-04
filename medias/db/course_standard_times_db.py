from db.db import singleton_ScrubDb
from common import common
from url.course_standard_times_url import CourseStandardTimesUrl


def exportToDb(course_standard_times_table_rows):
    if len(course_standard_times_table_rows) <= 0:
        return
    tableName = CourseStandardTimesUrl().EXPORT_TABLE
    __createTable(tableName)
    for row in course_standard_times_table_rows:
        try:
            singleton_ScrubDb.cursor.execute("select * from {} where track=%s and distance=%s".format(tableName),
                                             (row[0], row[1]))
            repetition = singleton_ScrubDb.cursor.fetchone()
            if repetition:
                sql_insert = """update {} set GroupRace=%s, cls_1=%s, cls_2=%s, cls_3=%s, cls_4=%s, 
                cls_5=%s, GriffinRace=%s where track=%s and distance=%s""".format(tableName)
                cur_list = row[2:]
                cur_list.append(row[0])
                cur_list.append(row[1])
                singleton_ScrubDb.cursor.execute(sql_insert, (cur_list))
            else:
                sql_insert = """insert into {}(track, distance, GroupRace, cls_1, cls_2, cls_3, cls_4, 
                cls_5, GriffinRace) value (%s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tableName)
                singleton_ScrubDb.cursor.execute(sql_insert, (row))
        except Exception as error:
            common.log('course standard times export to db error:' + str(error))
    singleton_ScrubDb.connect.commit()


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    track VARCHAR(45) DEFAULT '',
    distance INT DEFAULT 0,
    GroupRace VARCHAR(45) DEFAULT '',
    cls_1 VARCHAR(45) DEFAULT '',
    cls_2 VARCHAR(45) DEFAULT '',
    cls_3 VARCHAR(45) DEFAULT '',
    cls_4 VARCHAR(45) DEFAULT '',
    cls_5 VARCHAR(45) DEFAULT '',
    GriffinRace VARCHAR(45) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

