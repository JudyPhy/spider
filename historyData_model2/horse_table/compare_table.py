# ### 比对两张horse表，若一张包含另一张数据，则删除多余表 ###
# from db.database import singleton_Scrub_DB
# from common import common
# import csv
#
# # table1 相对 table2 更新时间较近
# TABLE1 = 'a_all_horse_info_20181113'
# TABLE2 = 'a_all_horse_info_20181112'
#
# FILENAME_SAME_HORSE_CODE = 'same_horse_code.csv'
#
# def getRowFromComparedTable(horse_code):
#     if singleton_Scrub_DB.table_exists(TABLE1):
#         singleton_Scrub_DB.cursor.execute('select * from {} where code=%s'.format(TABLE1), horse_code)
#         row = singleton_Scrub_DB.cursor.fetchone()
#         singleton_Scrub_DB.connect.commit()
#         return row
#     return None
#
# def compareTable():
#     sameHorseCodeList = []
#     if singleton_Scrub_DB.table_exists(TABLE2):
#         singleton_Scrub_DB.cursor.execute('select * from {}'.format(TABLE2))
#         list = singleton_Scrub_DB.cursor.fetchall()
#         singleton_Scrub_DB.connect.commit()
#
#         common.log('old table rows count=' + str(len(list)))
#         for row in list:
#             comparedData = getRowFromComparedTable(row['code'])
#             if not comparedData:
#                 continue
#             if comparedData['name'] != row['name']:
#                 common.log('code[' + row['code'] + '] ->name')
#                 continue
#             if comparedData['retired'] != row['retired']:
#                 common.log('code[' + row['code'] + '] ->retired')
#                 continue
#             if comparedData['country_of_origin'] != row['country_of_origin']:
#                 common.log('code[' + row['code'] + '] ->country_of_origin')
#                 continue
#             if comparedData['age'] != row['age']:
#                 common.log('code[' + row['code'] + '] ->age')
#                 continue
#             if comparedData['trainer'] != row['trainer']:
#                 common.log('code[' + row['code'] + '] ->trainer')
#                 continue
#             if comparedData['color'] != row['color']:
#                 common.log('code[' + row['code'] + '] ->color')
#                 continue
#             if comparedData['sex'] != row['sex']:
#                 common.log('code[' + row['code'] + '] ->sex')
#                 continue
#             if comparedData['owner'] != row['owner']:
#                 common.log('code[' + row['code'] + '] ->owner')
#                 continue
#             if comparedData['import_type'] != row['import_type']:
#                 common.log('code[' + row['code'] + '] ->import_type')
#                 continue
#             if comparedData['current_rating'] != row['current_rating']:
#                 common.log('code[' + row['code'] + '] ->current_rating' + '\n' + 'old:' + str(row['current_rating']) + ' new:' + str(comparedData['current_rating']) + '\n')
#                 continue
#             if comparedData['season_stakes'] != row['season_stakes']:
#                 common.log('code[' + row['code'] + '] ->season_stakes')
#                 continue
#             if comparedData['start_of_season_rating'] != row['start_of_season_rating']:
#                 common.log('code[' + row['code'] + '] ->start_of_season_rating')
#                 continue
#             if comparedData['total_stakes'] != row['total_stakes']:
#                 common.log('code[' + row['code'] + '] ->total_stakes')
#                 continue
#             if comparedData['No_1'] != row['No_1']:
#                 common.log('code[' + row['code'] + '] ->No_1')
#                 continue
#             if comparedData['No_2'] != row['No_2']:
#                 common.log('code[' + row['code'] + '] ->No_2')
#                 continue
#             if comparedData['No_3'] != row['No_3']:
#                 common.log('code[' + row['code'] + '] ->No_3')
#                 continue
#             if comparedData['No_of_starts'] != row['No_of_starts']:
#                 common.log('code[' + row['code'] + '] ->No_of_starts')
#                 continue
#             if comparedData['No_of_starts_in_past_10_race_meetings'] != row['No_of_starts_in_past_10_race_meetings']:
#                 common.log('code[' + row['code'] + '] ->No_of_starts_in_past_10_race_meetings')
#                 continue
#             if comparedData['sire'] != row['sire']:
#                 common.log('code[' + row['code'] + '] ->sire')
#                 continue
#             if comparedData['dam'] != row['dam']:
#                 common.log('code[' + row['code'] + '] ->dam')
#                 continue
#             if comparedData['dams_sire'] != row['dams_sire']:
#                 common.log('code[' + row['code'] + '] ->dams_sire')
#                 continue
#             if comparedData['same_sire'] != row['same_sire']:
#                 common.log('code[' + row['code'] + '] ->same_sire' + '\n' + 'old:' + row['same_sire'] + ' new:' + comparedData['same_sire'] + '\n')
#                 continue
#             if comparedData['current_location'] != row['current_location']:
#                 common.log('code[' + row['code'] + '] ->current_location' + '\n' + 'old:' + row['current_location'] + ' new:' + comparedData['current_location'] + '\n')
#                 continue
#             if comparedData['arrival_date'] != row['arrival_date']:
#                 common.log('code[' + row['code'] + '] ->arrival_date')
#                 continue
#             if comparedData['last_rating'] != row['last_rating']:
#                 common.log('code[' + row['code'] + '] ->last_rating')
#                 continue
#
#             #same data
#             sameHorseCodeList.append(row['code'])
#     else:
#         common.log('table[' + TABLE2 + '] not exist')
#
#     # exportSameCode(sameHorseCodeList)
#     common.log('same count=' + str(len(sameHorseCodeList)))
#
# def exportSameCode(codeList):
#     file = open(FILENAME_SAME_HORSE_CODE, 'a+', newline='')
#     writer = csv.writer(file)
#     for code in codeList:
#         writer.writerow([code])
#     file.close()
#
# if __name__ == '__main__':
#     compareTable()
#
#
