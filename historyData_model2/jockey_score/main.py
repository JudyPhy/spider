# ### 计算马匹评分、比赛场次、开始参赛时间，并存储至数据库中 ###
# from common import common
# from jockey_score.oneRace import OneRace
# from db.database import singleton_Results_DB
# from jockey_score.oneRace import singleton_JockeyScore
# import datetime
#
# # JOCKEY_SCORE_TABLE = singleton_cfg.getTempJockeyScoreExportTable()
#
#
# def getPlcDictOneRace(curRaceRows):
#     dict_plc = {}   # plc & [jockey, jockey, ...]
#     for row in curRaceRows:
#         if row['plc'] not in common.words:
#             plc = int(row['plc'].replace('DH', ''))
#             if plc not in dict_plc.keys():
#                 dict_plc[plc] = []
#             dict_plc[plc].append(row['jockey'].strip())
#     return dict_plc
#
#
# def getScoreDictOneRace(allScoreDict, curRaceRows):
#     dict_score = {}   # score & [jockey, jockey, ...]
#     for row in curRaceRows:
#         jockey = row['jockey'].strip()
#         if row['plc'] not in common.words:
#             if jockey in allScoreDict.keys():
#                 score = allScoreDict[jockey]
#             else:
#                 score = 0
#                 common.log('[getScoreDictOneRace]jockey[' + jockey + '] score not input to score map.')
#             if score not in dict_score:
#                 dict_score[score] = []
#             dict_score[score].append(jockey)
#     return dict_score
#
#
# # 计算评分
# def calculateScore(k):
#     dict_results = {}   # new_race_id & {jockey:score, jockey:score, ...}
#     singleton_Results_DB.cursor.execute(
#         '''select race_date,race_id,horse_code,jockey,plc from {} where race_date>=%s and race_date<=%s'''.format(RESULTS_FROM_TABLE),
#         (FROM_TIME_SCORE, TO_TIME_SCORE))
#     orig_list = singleton_Results_DB.cursor.fetchall()
#     singleton_Results_DB.connect.commit()
#
#     # 重组race_id并排序
#     dict_new_race_id = {}  # new_race_id & [row1, row2, ...]
#     for row in orig_list:
#         new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
#         if new_race_id not in dict_new_race_id.keys():
#             dict_new_race_id[new_race_id] = []
#         dict_new_race_id[new_race_id].append(row)
#     sorted_race_id_list = sorted(dict_new_race_id.keys())
#
#     # 计算每场比赛结束后的骑师分数
#     all_race_count = 0
#     right_race_count = 0
#     for curId in sorted_race_id_list:
#         rows_curRace = dict_new_race_id[curId]
#         if curId not in dict_results:
#             dict_results[curId] = {}
#
#         # 赛前，存储分数
#         for row in rows_curRace:
#             jockey = row['jockey'].strip()
#             if jockey not in singleton_JockeyScore.mapScore.keys():
#                 singleton_JockeyScore.setScore(jockey, common.JOCKEY_DEFAULT_SCORE)
#             jockey_horse = jockey + '(' + row['horse_code'] + ')'
#             dict_results[curId][jockey_horse] = singleton_JockeyScore.mapScore[jockey]
#
#         # 计算正确数量(不包括无效马)
#         # print('\nrace_id:', curId)
#         plc_dict = getPlcDictOneRace(rows_curRace)  # plc & [jockey, jockey, ...]
#         sorted_plc = sorted(plc_dict.keys())
#         # print('plc_dict:', plc_dict)
#         score_dict = getScoreDictOneRace(singleton_JockeyScore.mapScore, rows_curRace)   # score & [jockey, jockey, ...]
#         sorted_score = sorted(score_dict.keys())
#         sorted_score.reverse()
#         # index_score = 1
#         # for ss in sorted_score:
#         #     for j in score_dict[ss]:
#         #         print('score_dict:', index_score, ':', j, ' ', singleton_JockeyScore.mapScore[j])
#         #         index_score += 1
#
#         all_race_count += 1
#         jockeyList_plc123 = []
#         for plc in sorted_plc:
#             if plc > 3:
#                 break
#             jockeyList_plc123 += plc_dict[plc]
#         jockeyList_score123 = []
#         for score in sorted_score:
#             if len(jockeyList_score123) < 4:
#                 jockeyList_score123 += score_dict[score]
#             else:
#                 break
#         right = True
#         for targetCode in jockeyList_plc123:
#             if targetCode not in jockeyList_score123: # 前4个号中没有包含前三，则表示没中
#                 right = False
#                 break
#         if right:
#             right_race_count += 1
#
#         # 计算赛后分数
#         dict_curRace = {}   # jockey & plc
#         for row in rows_curRace:
#             key = row['jockey'].strip()
#             if row['plc'] not in common.words:
#                 dict_curRace[key] = row['plc']
#         OneRace(dict_curRace, k)
#         pass
#
#     # 计算总的正确率
#     score_rate = right_race_count / all_race_count * 100
#
#     return dict_results, score_rate
#
#
# def createScoreTable():
#     sql = '''create table if not exists {}(
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     race_id BIGINT DEFAULT 0,
#     jockey VARCHAR(128) DEFAULT '',
#     score INT DEFAULT 0)'''.format(JOCKEY_SCORE_TABLE)
#     singleton_Results_DB.cursor.execute(sql)
#
#
# def exportScoreResults(all_list):
#     if singleton_Results_DB.table_exists(JOCKEY_SCORE_TABLE):
#         singleton_Results_DB.cursor.execute('drop table {}'.format(JOCKEY_SCORE_TABLE))
#     createScoreTable()
#     sql = '''insert into {}(race_id, jockey, score)
#                 values (%s, %s, %s)'''.format(JOCKEY_SCORE_TABLE)
#     singleton_Results_DB.cursor.executemany(sql, all_list)
#     singleton_Results_DB.connect.commit()
#
#
# def exportCostTime(start_time):
#     end = datetime.datetime.now()
#     delta_time = end - start_time
#     print(delta_time.days, ' ', delta_time.seconds, ' ', delta_time.microseconds)
#
#
# def makeScoreTable():
#     K = 80
#     start_time = datetime.datetime.now()
#     dict_score, score_rate = calculateScore(K)  # new_race_id & {jockey:score, jockey:score, ...}
#     print('score_rate:', score_rate)
#
#     # 组装成批量数据结构
#     all_list = []
#     for raceId, dict in dict_score.items():
#         for key, score in dict.items():
#             item = (raceId, key, score)
#             all_list.append(item)
#
#     # 存储
#     exportScoreResults(all_list)
#     print('makeScoreTable over.')
#     exportCostTime(start_time)
#
#
# def calculateK():
#     max_rate = 0
#     k = 90
#     max_k = k
#     while (k <= 120):
#         singleton_JockeyScore.mapScore = {}
#         dict_score, score_rate = calculateScore(k)
#         if score_rate > max_rate:
#             max_rate = score_rate
#             max_k = k
#         print('k:', k, ' score_rate:', score_rate, ' max_rate:', max_rate, ' max_k:', max_k)
#         k += 1
#     print('max k:', max_k, ' max_rate:', max_rate)
#     # max k: 102  max_rate: 7.284056725397507 分数前四个号包含前三的马
#     # max k: 80  max_rate: 14.22432316287065 分数前五个号包含前三的马
#     # max k: 97  max_rate: 22.71164589600344 分数前六个号包含前三的马
#
#
# def main():
#     # calculateK()
#     makeScoreTable()
#
#
# # if __name__ == '__main__':
# #     main()
