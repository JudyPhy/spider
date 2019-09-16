from url.url_util import singleton_urlUtil
from url.horse_race_url import HorseRaceUrl
from url.race_results_url import RaceResultsUrl
from url.horse_pedigree_url import HorsePedigreeUrl
from url.display_sectional_time_url import DisplaySectionalTimeUrl
from url.race_card_url import RaceCardSpiderUrl
from url.race_dividend_url import RaceDividendUrl
from url.course_standard_times_url import CourseStandardTimesUrl
from url.sectional_odds_url import SectionalOddsUrl
import datetime
from common import common


class UrlManager(object):

    def GetRaceResultsUrlList(self, from_date, to_date, rmLoaded):
        start_year, start_month, start_day = singleton_urlUtil.getFromTime(from_date)
        end_year, end_month, end_day = singleton_urlUtil.getToTime(to_date)
        urlList = []
        for y in range(start_year, end_year + 1):
            start_m = 1
            end_m = 12
            if y == start_year:
                start_m = start_month
            if y == end_year:
                end_m = end_month
            for m in range(start_m, end_m + 1):
                start_d = 1
                end_d = 31
                if y == start_year and m == start_m:
                    start_d = start_day
                if y == end_year and m == end_m:
                    end_d = end_day
                for d in range(start_d, end_d + 1):
                    for r in range(1, 12):
                        for site in ['ST', 'HV']:
                            u = RaceResultsUrl().getUrl(y, m, d, site, r)
                            urlList.append(u)

        if rmLoaded == True:
            # 剔除已爬取的网址
            urlRmList = []
            loadedUrlList = RaceResultsUrl().getLoadedUrlList(start_year, end_year)
            for u in urlList:
                if u not in loadedUrlList:
                    urlRmList.append(u)
            print('race results url count=', len(urlRmList))
            return urlRmList
        else:
            print('race results url count=', len(urlList))
            return urlList

    def GetHorseRaceUrlList(self, from_date, to_date, rmLoaded):
        horse_code_list = singleton_urlUtil.getHorseCodeListByDateRange(from_date, to_date)
        urlList = []
        if rmLoaded == True:
            # 剔除已爬取的网址
            loadedCodeList = HorseRaceUrl().getLoadedHorseCodeList()
            for horse_code in horse_code_list:
                if horse_code not in loadedCodeList:
                    u = HorseRaceUrl().getUrl(horse_code)
                    urlList.append(u)
        else:
            for horse_code in horse_code_list:
                u = HorseRaceUrl().getUrl(horse_code)
                urlList.append(u)
        print('horse race url count=', len(urlList))
        return urlList

    def GetHorsePedigreeUrlList(self, from_date, to_date, rmLoaded):
        horse_code_list = singleton_urlUtil.getHorseCodeListByDateRange(from_date, to_date)
        future_horse_code_list = singleton_urlUtil.getFutureHorseCodeListByDateRange(from_date, to_date)
        all_horse_code_list = []
        for horse_code in horse_code_list:
            if horse_code not in all_horse_code_list:
                all_horse_code_list.append(horse_code)
        for horse_code in future_horse_code_list:
            if horse_code not in all_horse_code_list:
                all_horse_code_list.append(horse_code)
        race_date_id_No_dict = singleton_urlUtil.getAllRaceDateIdAndNoDict()
        urlList = []
        if rmLoaded == True:
            # 剔除已爬取的网址
            loadedCodeList = HorsePedigreeUrl().getLoadedHorseCodeList()
            for horse_code in all_horse_code_list:
                if horse_code not in loadedCodeList:
                    u = HorsePedigreeUrl().getUrl(horse_code, race_date_id_No_dict)
                    urlList.append(u)
        else:
            for horse_code in all_horse_code_list:
                u = HorsePedigreeUrl().getUrl(horse_code, race_date_id_No_dict)
                urlList.append(u)
        print('horse pedigree url count=', len(urlList))
        return urlList

    def GetDisplaySectionalTimeUrlList(self, from_date, to_date, rmLoaded):
        race_date_No_dict = singleton_urlUtil.getRaceDateAndNoDictByDateRange(from_date, to_date)
        urlList = []
        if rmLoaded == True:
            # 剔除已爬取的网址
            loadedRaceDateNoList = DisplaySectionalTimeUrl().getLoadedRaceDataAndNoDict()
            for race_date, max_race_No in race_date_No_dict.items():
                for race_No in range(1, max_race_No + 1):
                    if (race_date in loadedRaceDateNoList.keys()) and (race_No in loadedRaceDateNoList[race_date]):
                        continue
                    year = race_date[:len(race_date) - 4]
                    month = race_date[len(race_date) - 4: len(race_date) - 2]
                    day = race_date[len(race_date) - 2:]
                    date = day + '/' + month + '/' + year
                    u = DisplaySectionalTimeUrl().getUrl(date, race_No)
                    urlList.append(u)
        else:
            for race_date, max_race_No in race_date_No_dict.items():
                for race_No in range(1, max_race_No + 1):
                    year = race_date[:len(race_date) - 4]
                    month = race_date[len(race_date) - 4: len(race_date) - 2]
                    day = race_date[len(race_date) - 2:]
                    date = day + '/' + month + '/' + year
                    u = DisplaySectionalTimeUrl().getUrl(date, race_No)
                    urlList.append(u)
        print('display sectional time url count=', len(urlList))
        return urlList

    def GetHistoryRaceCardUrlList(self, from_date, to_date, rmLoaded):
        race_date_No_site_dict = singleton_urlUtil.getRaceDateAndNoSiteDictByDateRange(from_date, to_date)
        urlList = []
        if rmLoaded == True:
            # 剔除已爬取的网址
            loadedRaceDateNoList = RaceCardSpiderUrl().getLoadedHistoryRaceDataAndNoDict()
            for race_date, dict in race_date_No_site_dict.items():
                for race_No, site in dict.items():
                    if (race_date in loadedRaceDateNoList.keys()) and (race_No in loadedRaceDateNoList[race_date]):
                        continue
                    u = RaceCardSpiderUrl().getUrl(race_date, site, race_No)
                    urlList.append(u)
        else:
            for race_date, dict in race_date_No_site_dict.items():
                for race_No, site in dict.items():
                    u = RaceCardSpiderUrl().getUrl(race_date, site, race_No)
                    urlList.append(u)
        print('history race card url count=', len(urlList))
        return urlList

    def GetFutureRaceCardUrlList(self, days):
        urlList = []
        today = datetime.datetime.now()
        for deltaDay in range(days):
            detaday = datetime.timedelta(days=deltaDay)
            future = today + detaday
            race_date = str(future.year) + common.toDoubleDigitStr(future.month) + common.toDoubleDigitStr(future.day)
            for race_No in range(1, 12):
                for site in ['ST', 'HV']:
                    u = RaceCardSpiderUrl().getUrl(race_date, site, race_No)
                    urlList.append(u)
        print('future race card url count=', len(urlList))
        return urlList

    def GetSectionalOddsUrlList(self, from_date, to_date, rmLoaded):
        race_date_No_dict = singleton_urlUtil.getRaceDateAndNoDictByDateRange(from_date, to_date)
        urlList = []
        if rmLoaded == True:
            # 剔除已爬取的网址
            loadedRaceDateNoDict = SectionalOddsUrl().getLoadedRaceDataAndNoDict()
            for race_date, max_race_No in race_date_No_dict.items():
                for race_No in range(1, max_race_No + 1):
                    if (race_date in loadedRaceDateNoDict.keys()) and (race_No in loadedRaceDateNoDict[race_date]):
                        continue
                    u = SectionalOddsUrl().getUrl(race_date, race_No)
                    urlList.append(u)
        else:
            for race_date, max_race_No in race_date_No_dict.items():
                for race_No in range(1, max_race_No + 1):
                    u = SectionalOddsUrl().getUrl(race_date, race_No)
                    urlList.append(u)
        print('sectional odds url count=', len(urlList))
        return urlList

    def GetRaceDividendUrlList(self, from_date, to_date, rmLoaded):
        race_date_No_dict = singleton_urlUtil.getRaceDateAndNoDictByDateRange(from_date, to_date)
        urlList = []
        if rmLoaded == True:
            # 剔除已爬取的网址
            loadedRaceDateList = RaceDividendUrl().getLoadedRaceDateList()
            for race_date in race_date_No_dict.keys():
                if race_date in loadedRaceDateList:
                    continue
                u = RaceDividendUrl().getUrl(race_date)
                urlList.append(u)
        else:
            for race_date in race_date_No_dict.keys():
                u = RaceDividendUrl().getUrl(race_date)
                urlList.append(u)
        print('race dividend url count=', len(urlList))
        return urlList

    def GetCourseStandardTimesUrlList(self):
        urlList = []
        u = CourseStandardTimesUrl().getUrl()
        urlList.append(u)
        return urlList


singleton_url = UrlManager()

