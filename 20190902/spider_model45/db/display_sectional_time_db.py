from db.db import singleton_ScrubDb
from common import common
from url.display_sectional_time_url import DisplaySectionalTimeUrl


def exportToDb(race_info, sectional_time_table):
    if len(sectional_time_table) <= 0:
        return
    tableName = DisplaySectionalTimeUrl().EXPORT_TABLE
    __createTable(tableName)
    for row in sectional_time_table:
        try:
            singleton_ScrubDb.cursor.execute("select * from {} where race_date=%s and race_No=%s and horse_No=%s and horse_code=%s".format(tableName),
                                             (race_info['race_date'], race_info['race_No'], row['horse_No'], row['horse_code']))
            repetition = singleton_ScrubDb.cursor.fetchone()
            if repetition:
                pass
            else:
                sql_insert = """insert into {}(race_date, race_No, site, cls, distance, course, going,
                finishing_order, horse_No, horse, horse_code, 
                sec1_pos, sec1_i, sec1_time, sec2_pos, sec2_i, sec2_time, 
                sec3_pos, sec3_i, sec3_time, sec4_pos, sec4_i, sec4_time, 
                sec5_pos, sec5_i, sec5_time, sec6_pos, sec6_i, sec6_time, time)
                value (%s, %s, %s, %s, %s, %s, %s,  
                %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s)""".format(tableName)
                cur_list = [race_info['race_date'], race_info['race_No'], race_info['site'], race_info['cls'],
                                race_info['distance'], race_info['course'], race_info['going']]
                cur_list += list(row.values())
                singleton_ScrubDb.cursor.execute(sql_insert, (cur_list))
        except Exception as error:
            common.log('display sectional time export to db error:' + str(error))
    singleton_ScrubDb.connect.commit()


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_No INT DEFAULT 0,
    site VARCHAR(45) DEFAULT '',
    cls VARCHAR(45) DEFAULT '',
    distance VARCHAR(45) DEFAULT '',
    course VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',
    finishing_order VARCHAR(45) DEFAULT '',
    horse_No INT DEFAULT 0,
    horse VARCHAR(45) DEFAULT '',
    horse_code VARCHAR(45) DEFAULT '',    
    sec1_time VARCHAR(45) DEFAULT '',
    sec1_pos VARCHAR(45) DEFAULT '',
    sec1_i VARCHAR(45) DEFAULT '',
    sec2_time VARCHAR(45) DEFAULT '',
    sec2_pos VARCHAR(45) DEFAULT '',
    sec2_i VARCHAR(45) DEFAULT '',
    sec3_time VARCHAR(45) DEFAULT '',
    sec3_pos VARCHAR(45) DEFAULT '',
    sec3_i VARCHAR(45) DEFAULT '',
    sec4_time VARCHAR(45) DEFAULT '',
    sec4_pos VARCHAR(45) DEFAULT '',
    sec4_i VARCHAR(45) DEFAULT '',
    sec5_time VARCHAR(45) DEFAULT '',
    sec5_pos VARCHAR(45) DEFAULT '',
    sec5_i VARCHAR(45) DEFAULT '',
    sec6_time VARCHAR(45) DEFAULT '',
    sec6_pos VARCHAR(45) DEFAULT '',
    sec6_i VARCHAR(45) DEFAULT '',
    time VARCHAR(45) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

