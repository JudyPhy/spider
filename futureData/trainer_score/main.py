### ������ƥ���֡��������Ρ���ʼ����ʱ�䣬���洢�����ݿ��� ###
from common import common
from trainer_score.one_race import OneRace
from db.database import singleton_Results_DB
from trainer_score.one_race import singleton_TrainerScore
import datetime
from config.myconfig import singleton as singleton_cfg

TRAINER_SCORE_TABLE = singleton_cfg.getTempTrainerScoreExportTable()

RESULTS_FROM_TABLE = singleton_cfg.getCombineResultsExportTable()

FROM_TIME_SCORE = singleton_cfg.getDragonFromTime()
TO_TIME_SCORE = singleton_cfg.getDragonToTime()


def getPlcDictOneRace(curRaceRows):
    dict_plc = {}   # plc & [trainer, trainer, ...]
    for row in curRaceRows:
        if row['plc'] not in common.words:
            plc = int(row['plc'].replace('DH', ''))
            if plc not in dict_plc.keys():
                dict_plc[plc] = []
            dict_plc[plc].append(row['trainer'].strip())
    return dict_plc


def getScoreDictOneRace(allScoreDict, curRaceRows):
    dict_score = {}   # score & [trainer, trainer, ...]
    for row in curRaceRows:
        trainer = row['trainer'].strip()
        if row['plc'] not in common.words:
            if trainer in allScoreDict.keys():
                score = allScoreDict[trainer]
            else:
                score = 0
                common.log('[getScoreDictOneRace]trainer[' + trainer + '] score not input to score map.')
            if score not in dict_score:
                dict_score[score] = []
            dict_score[score].append(trainer)
    return dict_score


# ��������
def calculateScore(k):
    dict_results = {}   # new_race_id & {trainer:score, trainer:score, ...}
    singleton_Results_DB.cursor.execute(
        '''select race_date,race_id,horse_code,trainer,plc from {} where race_date>=%s and race_date<=%s'''.format(RESULTS_FROM_TABLE),
        (FROM_TIME_SCORE, TO_TIME_SCORE))
    orig_list = singleton_Results_DB.cursor.fetchall()
    singleton_Results_DB.connect.commit()

    # ����race_id������
    dict_new_race_id = {}  # new_race_id & [row1, row2, ...]
    for row in orig_list:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in dict_new_race_id.keys():
            dict_new_race_id[new_race_id] = []
        dict_new_race_id[new_race_id].append(row)
    sorted_race_id_list = sorted(dict_new_race_id.keys())

    # ����ÿ�����������������ʦ����
    all_race_count = 0
    right_race_count = 0
    for curId in sorted_race_id_list:
        rows_curRace = dict_new_race_id[curId]
        if curId not in dict_results:
            dict_results[curId] = {}

        # ��ǰ���洢����
        for row in rows_curRace:
            trainer = row['trainer'].strip()
            if trainer not in singleton_TrainerScore.mapScore.keys():
                singleton_TrainerScore.setScore(trainer, common.TRAINER_DEFAULT_SCORE)
            trainer_horse = trainer + '(' + row['horse_code'] + ')'
            dict_results[curId][trainer_horse] = singleton_TrainerScore.mapScore[trainer]

        # ������ȷ����(��������Ч��)
        # print('\nrace_id:', curId)
        plc_dict = getPlcDictOneRace(rows_curRace)  # plc & [trainer, trainer, ...]
        sorted_plc = sorted(plc_dict.keys())
        # print('plc_dict:', plc_dict)
        score_dict = getScoreDictOneRace(singleton_TrainerScore.mapScore, rows_curRace)   # score & [trainer, trainer, ...]
        sorted_score = sorted(score_dict.keys())
        sorted_score.reverse()
        # index_score = 1
        # for ss in sorted_score:
        #     for j in score_dict[ss]:
        #         print('score_dict:', index_score, ':', j, ' ', singleton_JockeyScore.mapScore[j])
        #         index_score += 1

        all_race_count += 1
        trainerList_plc123 = []
        for plc in sorted_plc:
            if plc > 3:
                break
            trainerList_plc123 += plc_dict[plc]
        trainerList_score123 = []
        for score in sorted_score:
            if len(trainerList_score123) < 4:
                trainerList_score123 += score_dict[score]
            else:
                break
        right = True
        for targetCode in trainerList_plc123:
            if targetCode not in trainerList_score123: # ǰ4������û�а���ǰ�������ʾû��
                right = False
                break
        if right:
            right_race_count += 1

        # �����������
        dict_curRace = {}   # trainer & plc
        for row in rows_curRace:
            key = row['trainer'].strip()
            if row['plc'] not in common.words:
                dict_curRace[key] = row['plc']
        OneRace(dict_curRace, k)
        pass

    # �����ܵ���ȷ��
    score_rate = right_race_count / all_race_count * 100

    return dict_results, score_rate


def createScoreTable():
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_id BIGINT DEFAULT 0,
    trainer VARCHAR(128) DEFAULT '',
    score INT DEFAULT 0)'''.format(TRAINER_SCORE_TABLE)
    singleton_Results_DB.cursor.execute(sql)


def exportScoreResults(all_list):
    if singleton_Results_DB.table_exists(TRAINER_SCORE_TABLE):
        singleton_Results_DB.cursor.execute('drop table {}'.format(TRAINER_SCORE_TABLE))
    createScoreTable()
    sql = '''insert into {}(race_id, trainer, score)
                values (%s, %s, %s)'''.format(TRAINER_SCORE_TABLE)
    singleton_Results_DB.cursor.executemany(sql, all_list)
    singleton_Results_DB.connect.commit()


def exportCostTime(start_time):
    end = datetime.datetime.now()
    delta_time = end - start_time
    print(delta_time.days, ' ', delta_time.seconds, ' ', delta_time.microseconds)


def makeScoreTable():
    K = 258
    start_time = datetime.datetime.now()
    dict_score, score_rate = calculateScore(K)  # new_race_id & {trainer:score, trainer:score, ...}
    print('score_rate:', score_rate)

    # ��װ���������ݽṹ
    all_list = []
    for raceId, dict in dict_score.items():
        for key, score in dict.items():
            item = (raceId, key, score)
            all_list.append(item)

    # �洢
    exportScoreResults(all_list)
    print('makeScoreTable over.')
    exportCostTime(start_time)


def calculateK():
    max_rate = 0
    k = 200
    max_k = k
    while (k <= 230):
        singleton_TrainerScore.mapScore = {}
        dict_score, score_rate = calculateScore(k)
        if score_rate > max_rate:
            max_rate = score_rate
            max_k = k
        print('k:', k, ' score_rate:', score_rate, ' max_rate:', max_rate, ' max_k:', max_k)
        k += 1
    print('max k:', max_k, ' max_rate:', max_rate)
    # max k: 292  max_rate: 3.5668242372152985 ����ǰ�ĸ��Ű���ǰ������
    # max k: 258  max_rate: 7.198109153416415 ����ǰ����Ű���ǰ������
    # max k: 211  max_rate: 13.021057155135368 ����ǰ�����Ű���ǰ������


def main():
    # calculateK()
    makeScoreTable()


# if __name__ == '__main__':
#     main()
