from common import common
import math


class OneRace(object):
    def __init__(self, oneRaceDict, k):
        self.k = k
        self.__calculateScore(oneRaceDict)

    # oneRaceDict: horse_code & plc
    def __calculateScore(self, oneRaceDict):
        check_e_list = []
        check_s_list = []
        count = len(oneRaceDict)
        fn = count * (count - 1) / 2
        temp_score_map = {}
        for curHorseCode, curHorsePlc in oneRaceDict.items():
            # ExPlus
            ExPlus = 0
            Rx = singleton_HorseScore.getHorseCurrentScore(curHorseCode)
            for otherHorseCode, otherHorsePlc in oneRaceDict.items():
                if curHorseCode != otherHorseCode:
                    Ri = singleton_HorseScore.getHorseCurrentScore(otherHorseCode)
                    y = (Ri - Rx)/400
                    ExPlus = ExPlus + 1 / (1 + math.pow(10, y))
                else:
                    pass

            # SxPlus
            if 'DH' in curHorsePlc:
                SxPlus = count - (int(curHorsePlc.replace('DH', '')) + 0.5)
            else:
                SxPlus = count - int(curHorsePlc)

            Ex = ExPlus / fn
            Sx = SxPlus / fn
            RxPlus = int(Rx + self.k * (Sx - Ex))
            temp_score_map[curHorseCode] = RxPlus

            check_e_list.append(Ex)
            check_s_list.append(Sx)

        for key, value in temp_score_map.items():
            singleton_HorseScore.setHorseScore(key, value)

        # 验证数据
        sum_e = 0
        sum_s = 0
        for e in check_e_list:
            sum_e += e
        for s in check_s_list:
            sum_s += s
        if math.fabs(sum_e - 1) > 0.01:
            pass
            # common.log('calculate e error:' + str(self.race_date) + ' ' + str(self.race_id) + ', e:' + str(sum_e))
        if math.fabs(sum_s - 1) > 0.01:
            pass
            # common.log('calculate s error: ' + str(self.race_date) + ' ' + str(self.race_id) + ', s:' + str(sum_s))


class HorseScoreManager(object):
    def __init__(self):
        self.mapScore = {}  # horse_code & score

    def getHorseCurrentScore(self, horse_code):
        if horse_code in self.mapScore.keys():
            return self.mapScore[horse_code]
        else:
            return common.HORSE_DEFAULT_SCORE

    def setHorseScore(self, horse_code, score):
        self.mapScore[horse_code] = score


singleton_HorseScore = HorseScoreManager()






