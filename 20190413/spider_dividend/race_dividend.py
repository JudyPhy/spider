from race_dividend_parse import RaceDividendsParse
from url.urlManager import singleton_url
from db import dividend_db
from chromeDriver import singleton_chrome
import time
from db.db import singleton_ScrubDb
from common import common


class RaceDividendSpider(object):

    def start_requests(self):
        urlList = singleton_url.getUrlList()
        for url in urlList:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.2)
            dividend = RaceDividendsParse(singleton_chrome.driver.page_source)
            if len(dividend.dividend_dict) > 0:
                # export
                race_date_No_id_dict = self.__getRaceDateNoAndIdDict()
                all_list = []
                for race_no, array in dividend.dividend_dict.items():
                    for item in array:
                        race_id = self.__getRaceId(dividend.race_date, race_no, race_date_No_id_dict)
                        year = int(dividend.race_date[len(dividend.race_date) - 6: len(dividend.race_date) - 4])
                        month = int(dividend.race_date[len(dividend.race_date) - 4: len(dividend.race_date) - 2])
                        if month < 8:
                            year -= 1
                        new_race_id = int(str(year) + common.toThreeDigitStr(race_id))
                        cur_line = (dividend.race_date, race_no, new_race_id, item['pool'], item['winning_combination'], item['dividend'])
                        all_list.append(cur_line)
                dividend_db.exportToDb(dividend.race_date, all_list)

    def __getRaceDateNoAndIdDict(self):
        dict = {}  # race_date & {race_No & race_id}
        for year in range(2014, 2020):
            tableName = 'f_race_results_{0}'.replace('{0}', str(year))
            singleton_ScrubDb.cursor.execute('select race_date,race_id,race_No from {}'.format(tableName))
            rows_results = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows_results:
                array_date = row['race_date'].split('/')
                race_date = array_date[2] + array_date[1] + array_date[0]
                if race_date not in dict.keys():
                    dict[race_date] = {}
                race_No = row['race_No']
                if race_No not in dict[race_date].keys():
                    race_id = row['race_id']
                    dict[race_date][race_No] = race_id
        return dict

    def __getRaceId(self, race_date, race_No, results_dict):
        if (race_date in results_dict.keys()) and (race_No in results_dict[race_date].keys()):
            return int(results_dict[race_date][race_No])
        if race_date == '20161026' and race_No == 4:
            return 134
        print('error race_id:', race_date, race_No)
        return 0

