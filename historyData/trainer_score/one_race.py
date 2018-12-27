from common import common
import math


class OneRace(object):
    def __init__(self, oneRaceDict, k):
        self.k = k
        self.__calculateScore(oneRaceDict)

    # oneRaceDict: trainer & plc
    def __calculateScore(self, oneRaceDict):
        check_e_list = []
        check_s_list = []
        count = len(oneRaceDict)
        fn = count * (count - 1) / 2
        temp_score_map = {}
        for curTrainer, curTrainerPlc in oneRaceDict.items():
            # ExPlus
            ExPlus = 0
            Rx = singleton_TrainerScore.getCurrentScore(curTrainer)
            for otherJockey, otherJockeyPlc in oneRaceDict.items():
                if curTrainer != otherJockey:
                    Ri = singleton_TrainerScore.getCurrentScore(otherJockey)
                    y = (Ri - Rx)/400
                    ExPlus = ExPlus + 1 / (1 + math.pow(10, y))
                else:
                    pass

            # SxPlus
            if 'DH' in curTrainerPlc:
                SxPlus = count - (int(curTrainerPlc.replace('DH', '')) + 0.5)
            else:
                SxPlus = count - int(curTrainerPlc)

            Ex = ExPlus / fn
            Sx = SxPlus / fn
            RxPlus = int(Rx + self.k * (Sx - Ex))
            temp_score_map[curTrainer] = RxPlus

            check_e_list.append(Ex)
            check_s_list.append(Sx)

        for key, value in temp_score_map.items():
            singleton_TrainerScore.setScore(key, value)

        # 验证数据
        sum_e = 0
        sum_s = 0
        for e in check_e_list:
            sum_e += e
        for s in check_s_list:
            sum_s += s
        if math.fabs(sum_e - 1) > 0.01:
            pass
            # common.log('calculate e error:' + ', e:' + str(sum_e))
        if math.fabs(sum_s - 1) > 0.01:
            pass
            # common.log('calculate s error: ' + ', s:' + str(sum_s))


class TrainerScoreManager(object):
    def __init__(self):
        self.mapScore = {}  # trainer & score

    def getCurrentScore(self, key):
        if key in self.mapScore.keys():
            return self.mapScore[key]
        else:
            return common.TRAINER_DEFAULT_SCORE

    def setScore(self, key, score):
        self.mapScore[key] = score


singleton_TrainerScore = TrainerScoreManager()






