### 合并马的最新数据，存储到export_table表中 ###
from db.database import singleton_Scrub_DB
from db.database import singleton_Results_DB
from common import common
import datetime
from config.myconfig import singleton_cfg

# f_all_horse_info、a_all_horse_info_20181112
SOURCE_TABLE_LIST = singleton_cfg.getCombineHorseSourceTableList() #按更新时间排序，最新的在最前面

EXPORT_TABLE = singleton_cfg.getCombineHorseExportTable()


def __getSourceData(tableName):
    all = []
    if singleton_Scrub_DB.table_exists(tableName):
        try:
            singleton_Scrub_DB.cursor.execute("select * from {}".format(tableName))
            all = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            return all
        except Exception as error:
            common.log('[combine_horse_tables]__getSourceData error:' + str(error))
    else:
        common.log('Table[' + tableName + '] not exist.')
    return all


def __createTable():
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45) DEFAULT '',
    code VARCHAR(45) DEFAULT '',
    retired INT DEFAULT 0,
    country_of_origin VARCHAR(45) DEFAULT '',
    age INT DEFAULT 0,
    trainer VARCHAR(45) DEFAULT '',
    color VARCHAR(45) DEFAULT '',
    sex VARCHAR(45) DEFAULT '',
    owner VARCHAR(1024) DEFAULT '',
    import_type VARCHAR(45) DEFAULT '',
    current_rating INT DEFAULT 0,
    season_stakes VARCHAR(45) DEFAULT '',
    start_of_season_rating INT DEFAULT 0,
    total_stakes VARCHAR(45) DEFAULT '',
    No_1 INT DEFAULT 0,
    No_2 INT DEFAULT 0,
    No_3 INT DEFAULT 0,
    No_of_starts INT DEFAULT 0,
    No_of_starts_in_past_10_race_meetings INT DEFAULT 0,
    sire VARCHAR(45) DEFAULT '',
    dam VARCHAR(45) DEFAULT '',
    dams_sire VARCHAR(45) DEFAULT '',
    same_sire VARCHAR(1024) DEFAULT '',
    current_location VARCHAR(45) DEFAULT '',
    arrival_date VARCHAR(45) DEFAULT '',
    last_rating VARCHAR(45) DEFAULT '')'''.format(EXPORT_TABLE)
    singleton_Results_DB.cursor.execute(sql)


def __getCombinedCodeList():
    codeList = []
    if singleton_Results_DB.table_exists(EXPORT_TABLE):
        singleton_Results_DB.cursor.execute("select code from {}".format(EXPORT_TABLE))
        all = singleton_Results_DB.cursor.fetchall()
        for row in all:
            codeList.append(row['code'])
        singleton_Results_DB.connect.commit()
    return codeList


def main():
    if singleton_Results_DB.table_exists(EXPORT_TABLE):
        singleton_Results_DB.cursor.execute('drop table {}'.format(EXPORT_TABLE))
        singleton_Results_DB.connect.commit()
    __createTable()
    for table in SOURCE_TABLE_LIST:
        combined_code_list = __getCombinedCodeList()
        source_list = __getSourceData(table)
        info_list = []
        for row in source_list:
            if row['code'] not in combined_code_list:
                cur_row_list = (row['name'], row['code'], row['retired'], row['country_of_origin'], row['age'],
                                row['trainer'], row['color'], row['sex'], row['owner'], row['import_type'],
                                row['current_rating'], row['season_stakes'], row['start_of_season_rating'], row['total_stakes'], row['No_1'],
                                row['No_2'], row['No_3'], row['No_of_starts'], row['No_of_starts_in_past_10_race_meetings'], row['sire'],
                                row['dam'], row['dams_sire'], row['same_sire'], row['current_location'], row['arrival_date'],
                                row['last_rating'])
                info_list.append(cur_row_list)

        sql = '''insert into {} (name, code, retired, country_of_origin, age, trainer, color, sex, owner, import_type,
                current_rating, season_stakes, start_of_season_rating, total_stakes, No_1, No_2, No_3, No_of_starts,
                No_of_starts_in_past_10_race_meetings, sire, dam, dams_sire, same_sire, current_location, arrival_date, last_rating)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s)'''.format(EXPORT_TABLE)
        singleton_Results_DB.cursor.executemany(sql, info_list)
        singleton_Results_DB.connect.commit()


# if __name__ == '__main__':
#     start = datetime.datetime.now()
#     main()
#     end = datetime.datetime.now()
#     delta_time = end - start
#     print(delta_time.days, ' ', delta_time.seconds, ' ', delta_time.microseconds)