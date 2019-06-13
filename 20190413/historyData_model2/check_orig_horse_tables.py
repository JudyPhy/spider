###  ###
from db.database import singleton_Scrub_DB
from common import common

TAG = '[check_orig_horse_tables]'


def getCodeDict(table):
    codeDict = {}
    if singleton_Scrub_DB.table_exists(table):
        singleton_Scrub_DB.cursor.execute('select code from {}'.format(table))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            if row['code'] not in codeDict.keys():
                codeDict[row['code']] = row
    return codeDict


def checkTableUse():
    orig_table_list = ['a_all_horse_info_20181203', 'a_all_horse_info_20181129', 'a_all_horse_info_20181128', 'a_horse_info_201811', 'a_all_horse_info_20181113']
    orig_table_list.reverse()
    cantExceptTableList = []
    for index in range(len(orig_table_list)):
        table = orig_table_list[index]
        codeList = getCodeDict(table).keys()
        for code in codeList:
            find = False
            for index_other in range(index + 1, len(orig_table_list)):
                table_other = orig_table_list[index_other]
                codeList_other = getCodeDict(table_other).keys()
                if code in codeList_other:
                    find = True
                    break
            if find == False:
                cantExceptTableList.append(table)
                break
    print('cantExceptTableList:', cantExceptTableList)


def compareTwoTable(table1, table2):
    codeDict_1 = getCodeDict(table1)
    codeDict_2 = getCodeDict(table2)
    print('codeDict_1:', len(codeDict_1), ' codeDict_2:', len(codeDict_2))
    repeatCodeList = []
    for code in codeDict_1.keys():
        if code in codeDict_2.keys():
            repeatCodeList.append(code)
    if len(repeatCodeList) == 0:
        pass
    else:
        print('table[', table1, '] and table[', table2, '] has ', len(repeatCodeList), ' repeated horse')


class CombineHorseTables(object):

    def __getSourceData(self, tableName):
        all = []
        if singleton_Scrub_DB.table_exists(tableName):
            try:
                singleton_Scrub_DB.cursor.execute("select * from {}".format(tableName))
                all = singleton_Scrub_DB.cursor.fetchall()
                singleton_Scrub_DB.connect.commit()
                return all
            except Exception as error:
                common.log(TAG + '__getSourceData error:' + str(error))
        else:
            common.log('Table[' + tableName + '] not exist.')
        return all

    def __createTable(self, exportTable):
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
        last_rating VARCHAR(45) DEFAULT '',
        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(exportTable)
        singleton_Scrub_DB.cursor.execute(sql)

    def combine(self, table1, table2, exportTable):
        if singleton_Scrub_DB.table_exists(exportTable):
            singleton_Scrub_DB.cursor.execute('drop table {}'.format(exportTable))
            singleton_Scrub_DB.connect.commit()
        self.__createTable(exportTable)
        info_list = []
        for table in [table1, table2]:
            source_list = self.__getSourceData(table)
            for row in source_list:
                row_list = list(row.values())[1:]
                for block in row_list:
                    if type(block) == type('a'):
                        block = block.replace(',', '|')
                cur_row_list = (row_list)
                print(cur_row_list)
                info_list.append(cur_row_list)

        sql = '''insert into {} (name, code, retired, country_of_origin, age, trainer, color, sex, owner, import_type,
        current_rating, season_stakes, start_of_season_rating, total_stakes, No_1, No_2, No_3, No_of_starts,
        No_of_starts_in_past_10_race_meetings, sire, dam, dams_sire, same_sire, current_location, arrival_date, last_rating)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s)'''.format(exportTable)
        singleton_Scrub_DB.cursor.executemany(sql, info_list)
        singleton_Scrub_DB.connect.commit()


def main():
    # compareTwoTable(SOURCE_TABLE_LIST[0], SOURCE_TABLE_LIST[1])
    checkTableUse()


main()