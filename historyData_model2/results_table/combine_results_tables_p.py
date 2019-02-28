### 合并原始数据，存储到export_table表中 ###
from db.database import singleton_Scrub_DB
from db.database import singleton_Results_DB
from common import common
import datetime
from config.myconfig import singleton_cfg


base_table = 'f_race_results_year'

FROM_TIME, TO_TIME = singleton_cfg.getCombineResultsTime()

EXPORT_TABLE = singleton_cfg.getCombineResultsExportTable()

def __toIntDate(str_date):
    array = str_date.split('/')
    if len(array) == 3:
        return int(array[2] + array[1] + array[0])
    else:
        common.log('race_date error:' + str_date)
        return 0


def __getSourceData(year):
    all = []
    tableName = base_table.replace('year', str(year))
    if singleton_Scrub_DB.table_exists(tableName):
        try:
            singleton_Scrub_DB.cursor.execute("select * from {}".format(tableName))
            all = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in all:
                # race_date 修改为整型，方便之后处理
                row['race_date'] = __toIntDate(row['race_date'])
        except Exception as error:
            common.log('[combine_results_tables]__getSourceData error:' + str(error))
    else:
        common.log('Table[' + tableName + '] not exist.')
    return all


def __createTable():
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date INT DEFAULT 0,
    race_id INT DEFAULT 0,
    race_No INT DEFAULT 0,
    site VARCHAR(45) DEFAULT '',
    cls VARCHAR(45) DEFAULT '',
    distance VARCHAR(45) DEFAULT '',
    bonus INT DEFAULT 0,
    course VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',
    plc VARCHAR(45) DEFAULT '',
    horse_No INT DEFAULT 0,
    horse VARCHAR(45) DEFAULT '',
    horse_code VARCHAR(45) DEFAULT '',
    jockey VARCHAR(45) DEFAULT '',
    trainer VARCHAR(45) DEFAULT '',
    actual_wt INT DEFAULT 0,
    declar_horse_wt VARCHAR(45) DEFAULT '',
    draw VARCHAR(45) DEFAULT '',
    lbw VARCHAR(45) DEFAULT '',
    running_position VARCHAR(45) DEFAULT '',
    finish_time VARCHAR(45) DEFAULT '',
    win_odds FLOAT DEFAULT 0.0)'''.format(EXPORT_TABLE)
    singleton_Results_DB.cursor.execute(sql)


def main():
    if singleton_Results_DB.table_exists(EXPORT_TABLE):
        singleton_Results_DB.cursor.execute('drop table {}'.format(EXPORT_TABLE))
        singleton_Results_DB.connect.commit()
    __createTable()
    sql = '''insert into {}(race_date, race_id, race_No, site, cls, distance, bonus, course, going,
                plc, horse_No, horse, horse_code, jockey, trainer, actual_wt, declar_horse_wt, draw, lbw, running_position, finish_time, win_odds)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(EXPORT_TABLE)
    # 历史数据
    for year in range(FROM_TIME, TO_TIME + 1):
        source_list = __getSourceData(year)
        cur_year_results_list = []
        for row in source_list:
            row_list = list(row.values())[1:]
            if 'updateTime' in row.keys():
                cur_row_list = (row_list[: len(cur_row_list)])
            else:
                cur_row_list = (row_list)
            cur_year_results_list.append(cur_row_list)
        singleton_Results_DB.cursor.executemany(sql, cur_year_results_list)
        singleton_Results_DB.connect.commit()