### 计算马匹评分、比赛场次、开始参赛时间，并存储至数据库中 ###
from common import common
from horse_score.one_race import OneRace
from horse_score.one_race import singleton_HorseScore
import datetime


# def getPlcDictOneRace(curRaceRows):
#     dict_plc = {}   # plc & [horse_code1, horse_code2, ...]
#     for row in curRaceRows:
#         if row['plc'] not in common.words:
#             plc = int(row['plc'].replace('DH', ''))
#             if plc not in dict_plc.keys():
#                 dict_plc[plc] = []
#             dict_plc[plc].append(row['horse_code'])
#     return dict_plc
#
#
# def getScoreDictOneRace(allScoreDict, curRaceRows):
#     dict_score = {}   # score & [horse_code1, horse_code2, ...]
#     for row in curRaceRows:
#         code = row['horse_code']
#         if row['plc'] not in common.words:
#             if code in allScoreDict.keys():
#                 score = allScoreDict[code]
#             else:
#                 score = 0
#                 common.log('[getScoreDictOneRace]horse[' + code + '] score not input to score map.')
#             if score not in dict_score:
#                 dict_score[score] = []
#             dict_score[score].append(code)
#     return dict_score


def __calculateScore(k, history_rows):
    # 按照比赛日期排序
    dict_new_race_id = {}  # new_race_id & [row1, row2, ...]
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in dict_new_race_id.keys():
            dict_new_race_id[new_race_id] = []
        dict_new_race_id[new_race_id].append(row)
    sorted_race_id_list = sorted(dict_new_race_id.keys())

    # 计算每场比赛结束后的马匹分数
    all_count = 0
    right_count = 0
    all_race_count = 0
    right_race_count = 0
    dict_results = {}  # new_race_id & {horse_code & score}
    for curId in sorted_race_id_list:
        rows_curRace = dict_new_race_id[curId]
        if curId not in dict_results.keys():
            dict_results[curId] = {}

        # 赛前
        for row in rows_curRace:
            code = row['horse_code']
            if code not in singleton_HorseScore.mapScore.keys():
                singleton_HorseScore.setHorseScore(code, common.HORSE_DEFAULT_SCORE)
            dict_results[curId][code] = singleton_HorseScore.mapScore[code]

        # # 计算正确数量(不包括无效马)
        # # for row in rows_curRace:
        # #     if row['plc'] not in common.words:
        # #         all_count += 1
        # plc_dict = getPlcDictOneRace(rows_curRace)  # plc & [horse_code1, horse_code2, ...]
        # sorted_plc = sorted(plc_dict.keys())
        # # print('plc_dict:', plc_dict)
        # score_dict = getScoreDictOneRace(singleton_HorseScore.mapScore, rows_curRace)   # score & [horse_code1, horse_code2, ...]
        # sorted_score = sorted(score_dict.keys())
        # sorted_score.reverse()
        # # print('score_dict:', score_dict)
        #
        # all_race_count += 1
        # codeList_plc123 = []
        # for plc in sorted_plc:
        #     if plc > 4:
        #         break
        #     codeList_plc123 += plc_dict[plc]
        # codeList_score123 = []
        # for score in sorted_score:
        #     if len(codeList_score123) < 5:
        #         codeList_score123 += score_dict[score]
        #     else:
        #         break
        # right = True
        # for targetCode in codeList_plc123:
        #     if targetCode not in codeList_score123: # 前4个号中没有包含前三，则表示没中
        #         right = False
        #         break
        # if right:
        #     right_race_count += 1
        #
        # # for plc in sorted_plc:
        # #     if plc > 4:
        # #         break
        # #     targetCodes = plc_dict[plc]
        # #     all_count += len(targetCodes)
        # #     index = 0
        # #     comparedCodes = []
        # #     for score in sorted_score:
        # #         if (plc > index) and (plc <= index + len(score_dict[score])):
        # #             comparedCodes = score_dict[score]
        # #         index += len(score_dict[score])
        # #
        # #     for targetCode in targetCodes:
        # #         if targetCode in comparedCodes:
        # #             right_count += 1

        # 赛后
        dict_curRace = {}   # horse_code & plc
        for row in rows_curRace:
            key = row['horse_code']
            if row['plc'] not in common.words:
                dict_curRace[key] = row['plc']
        OneRace(dict_curRace, k)
        pass

    # 计算总的正确率
    # print('all_race_count=', all_race_count, ' right_race_count=', right_race_count)
    # score_rate = right_count/all_count*100
    score_rate = 0#right_race_count / all_race_count * 100

    return dict_results, score_rate


def getHorseScoreDict(history_rows):
    K = 4454
    dict_score, score_rate = __calculateScore(K, history_rows)  # new_race_id & {horse_code & score}
    # print('score_rate:', score_rate)
    return dict_score


def calculateK():
    max_rate = 0
    k = 1000
    max_k = k
    while (k <= 5000):
        singleton_HorseScore.mapScore = {}
        dict_score, score_rate = __calculateScore(k)
        if score_rate > max_rate:
            max_rate = score_rate
            max_k = k
        print('k:', k, ' score_rate:', score_rate, ' max_rate:', max_rate, ' max_k:', max_k)
        k += 100
    print('max k:', max_k, ' max_rate:', max_rate)
    # max k: 3295  max_rate: 41.607040641099026 前三无序
    # max_k: 2553  max_rate: 50.08847659391924  前四无序
    # max k: 3043  max_rate: 15.662564396107614  前三有序
    # max k: 3392  max_rate: 14.746098986540835  前四有序

    # max k: 2616  max_rate: 11.989686291362268 分数前四个号包含前三的马
    # max k: 4454  max_rate: 20.885259991405242 分数前五个号包含前三的马
    # max k: 1966  max_rate: 31.75762784701332 分数前六个号包含前三的马

    # max k: 4600  max_rate: 9.260850880962613 分数前五个号包含前四的马
    # max k: 4130  max_rate: 17.855608079071768 分数前六个号包含前四的马

