from ..common import common
from ..config.myconfig import singleton_cfg
from ..db.db import singleton_ScrubDb

RACE_TYPE = ['ST', 'HV']

class UrlManager(object):

    def __getUrlByDateAndRaceNo(self, year, month, day, race_num):
        urlList = []
        time_str = str(year) + common.toDoubleDigitStr(month) + common.toDoubleDigitStr(day)
        for type in RACE_TYPE:
            u = singleton_cfg.getBaseUrl() + '/' + time_str + '/' + type + '/' + str(race_num)
            urlList.append(u)
        return urlList


    def __parseTime(self, str_time):
        array = str_time.split('-')
        if len(array) == 3:
            return int(array[0]), int(array[1]), int(array[2])
        return 0, 0, 0

    def __getFromRaceNo(self, str_raceNo):
        no = int(str_raceNo)
        if no != 0:
            return no
        else:
            return 1

    def __getToRanceNo(self, str_raceNo):
        no = int(str_raceNo)
        if no != 0:
            return no
        else:
            return 11

    def getUrlList(self):
        # time
        str_request_day = singleton_cfg.getRequestDay()
        request_year, request_month, request_day = self.__parseTime(str_request_day)
        # race No
        str_from_raceNo, str_to_raceNo = singleton_cfg.getRaceNo()
        start_raceNo = self.__getFromRaceNo(str_from_raceNo)
        end_raceNo = self.__getToRanceNo(str_to_raceNo)
        # url
        urlList = []
        if request_year != 0 and request_month != 0 and request_day != 0:
            for r in range(start_raceNo, end_raceNo + 1):
                list = self.__getUrlByDateAndRaceNo(request_year, request_month, request_day, r)
                urlList += list
        common.log('all race-card url count=' + str(len(urlList)))
        return urlList


singleton = UrlManager()

