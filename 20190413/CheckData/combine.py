from db.db import singleton_ScrubDB
# #
# #
# # def __createHorseInfoTable(tableName):
# #     sql = '''create table if not exists {}(
# #         id INT PRIMARY KEY AUTO_INCREMENT,
# #         race_date VARCHAR(45) DEFAULT '',
# #         race_time VARCHAR(45) DEFAULT '',
# #         race_id INT DEFAULT 0,
# #         race_No INT DEFAULT 0,
# #         site VARCHAR(45) DEFAULT '',
# #         cls VARCHAR(45) DEFAULT '',
# #         distance VARCHAR(45) DEFAULT '',
# #         bonus INT DEFAULT 0,
# #         course VARCHAR(45) DEFAULT '',
# #         going VARCHAR(45) DEFAULT '',
# #         horse_No INT DEFAULT 0,
# #         last_6_runs VARCHAR(45) DEFAULT '',
# #         horse VARCHAR(45) DEFAULT '',
# #         horse_code VARCHAR(45) DEFAULT '',
# #         wt VARCHAR(45) DEFAULT '',
# #         jockey VARCHAR(45) DEFAULT '',
# #         over_wt VARCHAR(45) DEFAULT '',
# #         draw VARCHAR(45) DEFAULT '',
# #         trainer VARCHAR(45) DEFAULT '',
# #         rtg VARCHAR(45) DEFAULT '',
# #         rtg_as VARCHAR(45) DEFAULT '',
# #         horse_wt_dec VARCHAR(45) DEFAULT '',
# #         wt_as_dec VARCHAR(45) DEFAULT '',
# #         best_time VARCHAR(45) DEFAULT '',
# #         age INT DEFAULT 0,
# #         wfa VARCHAR(45) DEFAULT '',
# #         sex VARCHAR(45) DEFAULT '',
# #         season_stacks VARCHAR(45) DEFAULT '',
# #         priority VARCHAR(45) DEFAULT '',
# #         gear VARCHAR(45) DEFAULT '',
# #         owner VARCHAR(256) DEFAULT '',
# #         sire VARCHAR(128) DEFAULT '',
# #         dam VARCHAR(128) DEFAULT '',
# #         import_cat VARCHAR(45) DEFAULT '',
# #         updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
# #     singleton_ScrubDB.cursor.execute(sql)
# #
# #
# # def __getSourceData(race_date):
# #     all = []
# #     tableName = 't_race_card_' + str(race_date)
# #     if singleton_ScrubDB.table_exists(tableName):
# #         singleton_ScrubDB.cursor.execute("select * from {}".format(tableName))
# #         all = singleton_ScrubDB.cursor.fetchall()
# #         singleton_ScrubDB.connect.commit()
# #     else:
# #         print('Table[' + tableName + '] not exist.')
# #     return all
# #
# #
# # def main():
# #     race_date = 20181205
# #     str_race_date = str(race_date)
# #     source_list = __getSourceData(race_date)
# #
# #     tableName = 't_race_card_future_2018'
# #     __createHorseInfoTable(tableName)
# #     sql = '''insert into {}(race_date, race_time, race_id, race_No, site, cls, distance, bonus, course, going,
# #                 horse_No, last_6_runs, horse, horse_code, wt, jockey, over_wt, draw, trainer, rtg,
# #                 rtg_as, horse_wt_dec, wt_as_dec, best_time, age, wfa, sex, season_stacks, priority,
# #                 gear, owner, sire, dam, import_cat)
# #                 values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
# #                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
# #                 %s, %s, %s, %s, %s, %s, %s, %s, %s,
# #                 %s, %s, %s, %s, %s)'''.format(tableName)
# #     cur_year_results_list = []
# #     for row in source_list:
# #         row_list = list(row.values())[1:]
# #         row_list.insert(1, 0)
# #         if 'updateTime' in row.keys():
# #             cur_row_list = (row_list[: len(row_list) - 1])
# #         else:
# #             cur_row_list = (row_list)
# #         # print(cur_row_list)
# #         cur_year_results_list.append(cur_row_list)
# #     singleton_ScrubDB.cursor.executemany(sql, cur_year_results_list)
# #     singleton_ScrubDB.connect.commit()
# #
# #
#
# # def main():
# #     tableName = 'g_display_sectional_time_2018'
# #     race_date = ['01/07/2018']
# #     for date in race_date:
# #         singleton_ScrubDB.cursor.execute('select race_No,going, course from {} where race_date=%s'.format(tableName), date)
# #         rows = singleton_ScrubDB.cursor.fetchall()
# #         singleton_ScrubDB.connect.commit()
# #         update_race_No = []   #1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
# #         for row in rows:
# #             race_No = row['race_No']
# #             if race_No not in update_race_No and race_No == 4:
# #                 update_race_No.append(race_No)
# #                 going = row['going']
# #                 course = row['course']
# #                 print(race_No, 'going:', going, ' course:', course)
# #
# #                 singleton_ScrubDB.cursor.execute('update {} set going=%s,course=%s where race_date=%s and race_No=%s'.format(tableName),
# #                                                  (course, going, date, race_No))
# #                 singleton_ScrubDB.connect.commit()
# #         print(update_race_No)
# from common import common
#
# def getRaceDateNoAndIdDict():
#     dict = {}   # race_date & {race_No & race_id}
#     for year in range(2014, 2020):
#         tableName = 'f_race_results_{0}'.replace('{0}', str(year))
#         singleton_ScrubDB.cursor.execute('select race_date,race_id,race_No from {}'.format(tableName))
#         rows_results = singleton_ScrubDB.cursor.fetchall()
#         singleton_ScrubDB.connect.commit()
#         for row in rows_results:
#             array_date = row['race_date'].split('/')
#             race_date = array_date[2] + array_date[1] + array_date[0]
#             if race_date not in dict.keys():
#                 dict[race_date] = {}
#             race_No = row['race_No']
#             if race_No not in dict[race_date].keys():
#                 race_id = row['race_id']
#                 dict[race_date][race_No] = race_id
#     return dict
#
# def getRaceId(race_date, race_No, results_dict):
#     if (race_date in results_dict.keys()) and (race_No in results_dict[race_date].keys()):
#         return int(results_dict[race_date][race_No])
#     if race_date == '20161026' and race_No == 4:
#         return 134
#     print('error race_id:', race_date, race_No)
#     return 0
#
# def createTable(tableName):
#     sql = '''create table if not exists {}(
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     race_date VARCHAR(45) DEFAULT '',
#     race_No INT DEFAULT 0,
#     race_id BIGINT DEFAULT 0,
#     pool VARCHAR(45) DEFAULT '',
#     winning_combination VARCHAR(45) DEFAULT '',
#     dividend VARCHAR(128) DEFAULT '')'''.format(tableName)
#     singleton_ScrubDB.cursor.execute(sql)
#
# def main():
#     results_dict = getRaceDateNoAndIdDict()
#     singleton_ScrubDB.cursor.execute('select * from b_race_dividend')
#     rows_dividend = singleton_ScrubDB.cursor.fetchall()
#     singleton_ScrubDB.connect.commit()
#     all_list = []
#     for row in rows_dividend:
#         race_date = row['race_date']
#         race_No  = row['race_No']
#         race_id = getRaceId(race_date, race_No, results_dict)
#         year = int(race_date[len(race_date) - 6: len(race_date) - 4])
#         month = int(race_date[len(race_date) - 4: len(race_date) - 2])
#         if month < 8:
#             year -= 1
#         new_race_id = int(str(year) + common.toThreeDigitStr(race_id))
#         cur_line = (race_date, race_No, new_race_id, row['pool'], row['winning_combination'], row['dividend'])
#         all_list.append(cur_line)
#
#     exportTable = 'bb_race_dividend'
#     createTable(exportTable)
#     inster_sql = '''insert into {}(race_date, race_No, race_id, pool, winning_combination, dividend)
#     values (%s, %s, %s, %s, %s, %s)'''.format(exportTable)
#     singleton_ScrubDB.cursor.executemany(inster_sql, all_list)
#     singleton_ScrubDB.connect.commit()
#
# main()

