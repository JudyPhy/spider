from common import common
import math


class OneRace(object):
    def __init__(self, oneRaceDict, k):
        self.k = k
        self.__calculateScore(oneRaceDict)

    # oneRaceDict: jockey & plc
    def __calculateScore(self, oneRaceDict):
        check_e_list = []
        check_s_list = []
        count = len(oneRaceDict)
        fn = count * (count - 1) / 2
        temp_score_map = {}
        for curJockey, curJockeyPlc in oneRaceDict.items():
            # ExPlus
            ExPlus = 0
            Rx = singleton_JockeyScore.getCurrentScore(curJockey)
            for otherJockey, otherJockeyPlc in oneRaceDict.items():
                if curJockey != otherJockey:
                    Ri = singleton_JockeyScore.getCurrentScore(otherJockey)
                    y = (Ri - Rx)/400
                    ExPlus = ExPlus + 1 / (1 + math.pow(10, y))
                else:
                    pass

            # SxPlus
            if 'DH' in curJockeyPlc:
                SxPlus = count - (int(curJockeyPlc.replace('DH', '')) + 0.5)
            else:
                SxPlus = count - int(curJockeyPlc)

            Ex = ExPlus / fn
            Sx = SxPlus / fn
            RxPlus = int(Rx + self.k * (Sx - Ex))
            temp_score_map[curJockey] = RxPlus

            check_e_list.append(Ex)
            check_s_list.append(Sx)

        for key_jockey, value_score in temp_score_map.items():
            singleton_JockeyScore.setScore(key_jockey, value_score)

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


class JockeyScoreManager(object):
    def __init__(self):
        self.mapScore = {}  # jockey & score

    def getCurrentScore(self, key):
        if key in self.mapScore.keys():
            return self.mapScore[key]
        else:
            return common.JOCKEY_DEFAULT_SCORE

    def setScore(self, key, score):
        self.mapScore[key] = score


singleton_JockeyScore = JockeyScoreManager()






