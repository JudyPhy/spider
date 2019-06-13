from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
from db.db import singleton_ScrubDb
import time
from lxml import etree
from db import race_dividend_db
from url.race_results_url import RaceResultsUrl


class RaceDividendSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        url_list = singleton_url.GetRaceDividendUrlList(self.from_date, self.to_date, self.rmLoaded)
        race_date_No_id_dict = self.__getRaceDateNoAndIdDict()
        for url in url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            race_dividend_parse = RaceDividendParse(singleton_chrome.driver.page_source)
            race_dividend_db.exportToDb(race_dividend_parse.race_date, race_dividend_parse.dividend_dict, race_date_No_id_dict)

    def __getRaceDateNoAndIdDict(self):
        dict = {}  # race_date & {race_No & race_id}
        singleton_ScrubDb.cursor.execute('select race_date,race_id,race_No from {}'.format(RaceResultsUrl().EXPORT_TABLE))
        rows_results = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows_results:
            race_date = row['race_date']
            if race_date not in dict.keys():
                dict[race_date] = {}
            race_No = row['race_No']
            if race_No not in dict[race_date].keys():
                race_id = row['race_id']
                dict[race_date][race_No] = race_id
        return dict


class RaceDividendParse(object):

    def __init__(self, page_source):
        self.race_date = ''
        self.dividend_dict = {}
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        # race info
        race_date_div = html.xpath('//td[@class="tdAlignL number13 color_black"]')
        race_date_text = race_date_div[0].xpath('string(.)')
        array_date = race_date_text.split(':')[1].split('/')
        self.race_date = array_date[2].strip() + array_date[1].strip() + array_date[0].strip()

        race_No_divs = html.xpath('//div[@class="boldFont13 color_white trBgBlue clearDivFloat lineH20"]')
        dividend_tables = html.xpath('//table[@class="trBgBlue tdAlignC font13 fontStyle"]')
        for race_No_div in race_No_divs:
            race_No = int(race_No_div.xpath('string(.)').replace('Race', ''))
            self.dividend_dict[race_No] = []
            trs = dividend_tables[race_No - 1].xpath('.//tr')

            cur_pool = ''
            for tr in trs[2:]:
                title = tr.xpath('./td/@rowspan')
                tds = tr.xpath('./td')
                startIndex = 0
                if len(title) > 0:
                    startIndex = 1
                    cur_pool = tds[0].xpath('string(.)').strip()
                cur_row = {}
                cur_row['pool'] = cur_pool
                cur_row['winning_combination'] = tds[startIndex].xpath('string(.)').strip()
                cur_row['dividend'] = tds[startIndex + 1].xpath('string(.)').replace(',', '').strip()
                self.dividend_dict[race_No].append(cur_row)

        # log
        for race_no, array in self.dividend_dict.items():
            print('race_no=', race_no)
            for item in array:
                print(item)

