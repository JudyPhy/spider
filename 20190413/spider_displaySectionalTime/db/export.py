from db.db import singleton_ScrubDb
from config.myconfig import singleton_cfg
from common import common


def exportSectionalTime(raceInfo, info_list):
    str_date = raceInfo['race_date'].split('/')
    tableName = singleton_cfg.getTargetExportTable(int(str_date[2]))
    __createSectionalTimeTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute(
            """select * from {} where race_date=%s and race_No=%s""".format(tableName), (raceInfo['race_date'], raceInfo['race_No']))
        rows = singleton_ScrubDb.cursor.fetchall()
        if len(rows) == len(info_list):
            pass
        else:
            singleton_ScrubDb.cursor.execute(
                """delete from {} where race_date=%s and race_No=%s""".format(tableName), (raceInfo['race_date'], raceInfo['race_No']))
            sql = """insert into {}(race_date, race_No, site, cls, distance, course, going,
            finishing_order, horse_No, horse, horse_code, 
            sec1_time, sec2_time, sec3_time, sec4_time, sec5_time, sec6_time, 
            sec1_pos, sec2_pos, sec3_pos, sec4_pos, sec5_pos, sec6_pos, 
            sec1_i, sec2_i, sec3_i, sec4_i, sec5_i, sec6_i, time)
            value (%s, %s, %s, %s, %s, %s, %s,  
            %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s)""".format(tableName)
            singleton_ScrubDb.cursor.executemany(sql, info_list)
        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log('[export]exportSectionalTime error:' + str(error))


def __createSectionalTimeTable(tableName):
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


