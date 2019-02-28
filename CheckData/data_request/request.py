from data_request.db import singleton_ResultsDB
import datetime
from data_request.myconfig import singleton as singleton_cfg
from data_request import common


class RequestData(object):

    # def __parseTime(self, time):
    #     array = time.split('-')
    #     if len(array) == 3:
    #         return int(array[0]), int(array[1]), int(array[2])
    #     else:
    #         return 0, 0, 0
    #
    # def __getFromTime(self, year, month, day):
    #     if year != 0:
    #         if month != 0:
    #             if day != 0:
    #                 return year, month, day
    #             else:
    #                 return year, month, 1
    #         else:
    #             if day != 0:
    #                 return year, 1, day
    #             else:
    #                 return year, 1, 1
    #     return datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day
    #
    # def __getToTime(self, year, month, day):
    #     if year != 0:
    #         if month != 0:
    #             if day != 0:
    #                 return year, month, day
    #             else:
    #                 return year, month, 31
    #         else:
    #             if day != 0:
    #                 return year, 12, day
    #             else:
    #                 return year, 12, 31
    #     return datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day
    #
    # def __searchData(self, race_date):
    #     tableName = singleton_cfg.getResultsTable()
    #     if singleton_ResultsDB.table_exists(tableName):
    #         try:
    #             singleton_ResultsDB.cursor.execute("select * from {} where race_date=%s".format(tableName), race_date)
    #             rows = singleton_ResultsDB.cursor.fetchall()
    #             singleton_ResultsDB.connect.commit()
    #             return rows
    #         except Exception as error:
    #             print(error)
    #
    #     return None

    # def getDataList(self, from_time, to_time):
    #     results = []
    #     arg1_from, arg2_from, arg3_from =  self.__parseTime(from_time)
    #     from_year, from_month, from_day = self.__getFromTime(arg1_from, arg2_from, arg3_from)
    #     arg1_to, arg2_to, arg3_to = self.__parseTime(to_time)
    #     to_year, to_month, to_day = self.__getToTime(arg1_to, arg2_to, arg3_to)
    #     for year in range(from_year, to_year + 1):
    #         for month in range(from_month, to_month + 1):
    #             for day in range(from_day, to_day + 1):
    #                 str_race_date = str(year) + common.toDoubleDigitStr(month) + common.toDoubleDigitStr(day)
    #                 race_date = int(str_race_date)
    #                 data = self.__searchData(race_date)
    #                 results += data
    #     return results

    def getDataList(self, from_time, to_time):
        results = []
        tableName = singleton_cfg.getResultsTable()
        if singleton_ResultsDB.table_exists(tableName):
            try:
                singleton_ResultsDB.cursor.execute("select * from {} where race_date>=%s and race_date<=%s".format(tableName), (from_time, to_time))
                results = singleton_ResultsDB.cursor.fetchall()
                singleton_ResultsDB.connect.commit()
            except Exception as error:
                print(error)

        return results
