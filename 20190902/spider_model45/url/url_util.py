import datetime
from db.db import singleton_ScrubDb
from common import common
from url.horse_race_url import HorseRaceUrl
from url.race_results_url import RaceResultsUrl
from url.race_card_url import RaceCardSpiderUrl


class UrlUtil(object):

    def __parseTime(self, str_time):
        array = str_time.split('-')
        if len(array) == 3:
            return int(array[0]), int(array[1]), int(array[2])
        return None, None, None

    def getFromTime(self, str_time):
        year, month, day = self.__parseTime(str_time)
        if year != 0:
            if month != 0:
                if day != 0:
                    return year, month, day
                else:
                    return year, month, 1
            else:
                if day != 0:
                    return year, 1, day
                else:
                    return year, 1, 1
        else:
            return None, None, None

    def getToTime(self, str_time):
        year, month, day = self.__parseTime(str_time)
        if year != 0:
            if month != 0:
                if day != 0:
                    return year, month, day
                else:
                    return year, month, 31
            else:
                if day != 0:
                    return year, 12, day
                else:
                    return year, 12, 31
        else:
            return None, None, None

    def getYMDDate(self, str_time):
        year, month, day = self.__parseTime(str_time)
        return str(year) + common.toDoubleDigitStr(month) + common.toDoubleDigitStr(day)

    def getHorseCodeListByDateRange(self, from_date, to_date):
        race_results_list = self.__requestRaceResultsListByDateRange(from_date, to_date)
        horse_code_list = []
        for row in race_results_list:
            horse_code = row['horse_code'].strip()
            if horse_code not in horse_code_list:
                horse_code_list.append(horse_code)
        print(from_date, ' ~ ', to_date, ' has ', len(horse_code_list), ' horses.')
        return horse_code_list

    def getFutureHorseCodeListByDateRange(self, from_date, to_date):
        future_race_card_list = self.__requestFutureRaceCardListByDateRange(from_date, to_date)
        horse_code_list = []
        for row in future_race_card_list:
            horse_code = row['horse_code'].strip()
            if horse_code not in horse_code_list:
                horse_code_list.append(horse_code)
        print(from_date, ' ~ ', to_date, ' future race has ', len(horse_code_list), ' horses.')
        return horse_code_list

    def getAllRaceDateIdAndNoDict(self):
        today = datetime.datetime.now()
        toDate = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
        race_results_list = self.__requestRaceResultsListByDateRange('2000-0-0', toDate)
        race_date_id_No_dict = {}   # race_date & {race_id & race_No}
        for row in race_results_list:
            race_date = row['race_date']
            if race_date not in race_date_id_No_dict.keys():
                race_date_id_No_dict[race_date] = {}
            race_id = row['race_id']
            race_No = row['race_No']
            race_date_id_No_dict[race_date][race_id] = race_No
        return race_date_id_No_dict

    def getRaceDateAndNoDictByDateRange(self, from_date, to_date):
        race_results_list = self.__requestRaceResultsListByDateRange(from_date, to_date)
        race_date_No_dict = {}  # race_date & max_race_No
        for row in race_results_list:
            race_date = row['race_date'].strip()
            race_No = row['race_No']
            if race_date not in race_date_No_dict.keys():
                race_date_No_dict[race_date] = 0
            if race_No > race_date_No_dict[race_date]:
                race_date_No_dict[race_date] = race_No

        # log
        count = 0
        for race_date, max_race_No in race_date_No_dict.items():
            count += max_race_No
        print(from_date, ' ~ ', to_date, ' has ', count, ' race_No items.')
        return race_date_No_dict

    def getRaceDateAndNoSiteDictByDateRange(self, from_date, to_date):
        race_results_list = self.__requestRaceResultsListByDateRange(from_date, to_date)
        race_date_No_site_dict = {}  # race_date & {race_No & site}
        for row in race_results_list:
            race_date = row['race_date'].strip()
            race_No = row['race_No']
            site = row['site'].replace(' ', '')
            if 'ShaTin' in site:
                site = 'ST'
            elif 'HappyValley' in site:
                site = 'HV'
            if race_date not in race_date_No_site_dict.keys():
                race_date_No_site_dict[race_date] = {}
            race_date_No_site_dict[race_date][race_No] = site

        print(from_date, ' ~ ', to_date, ' has ', len(race_date_No_site_dict), ' days race.')
        return race_date_No_site_dict

    def __requestRaceResultsListByDateRange(self, from_date, to_date):
        race_results_list = []
        start_year, start_month, start_day = self.getFromTime(from_date)
        end_year, end_month, end_day = self.getToTime(to_date)
        start_date = str(start_year) + common.toDoubleDigitStr(start_month) + common.toDoubleDigitStr(start_day)
        end_date = str(end_year) + common.toDoubleDigitStr(end_month) + common.toDoubleDigitStr(end_day)
        tableName = RaceResultsUrl().EXPORT_TABLE
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select * from {} where race_date>=%s and race_date<=%s'.format(tableName),
                                             (start_date, end_date))
            race_results_list = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
        else:
            print('table[', tableName, '] not exist')
        print(from_date, ' ~ ', to_date, ' has ', len(race_results_list), ' race results items.')
        return race_results_list

    def __requestHorseRaceListByDateRange(self, from_date, to_date):
        horse_code_list = self.getHorseCodeListByDateRange(from_date, to_date)
        horse_race_list = []
        for horse_code in horse_code_list:
            tableName = HorseRaceUrl().EXPORT_TABLE
            if singleton_ScrubDb.table_exists(tableName):
                singleton_ScrubDb.cursor.execute('select * from {} where code=%s'.format(tableName), horse_code)
                rows = singleton_ScrubDb.cursor.fetchall()
                for row in rows:
                    horse_race_list.append(row)
            else:
                print('table[', tableName, '] not exist')
        singleton_ScrubDb.connect.commit()
        return horse_race_list

    def __requestFutureRaceCardListByDateRange(self, from_date, to_date):
        future_race_card_list = []
        start_year, start_month, start_day = self.getFromTime(from_date)
        end_year, end_month, end_day = self.getToTime(to_date)
        start_date = str(start_year) + common.toDoubleDigitStr(start_month) + common.toDoubleDigitStr(start_day)
        end_date = str(end_year) + common.toDoubleDigitStr(end_month) + common.toDoubleDigitStr(end_day)
        tableName = RaceCardSpiderUrl().FUTURE_EXPORT_TABLE
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select * from {} where race_date>=%s and race_date<=%s'.format(tableName),
                                             (start_date, end_date))
            future_race_card_list = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
        else:
            print('table[', tableName, '] not exist')
        print(from_date, ' ~ ', to_date, ' has ', len(future_race_card_list), ' future race card items.')
        return future_race_card_list


singleton_urlUtil = UrlUtil()

