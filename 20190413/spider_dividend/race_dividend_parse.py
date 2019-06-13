from lxml import etree


class RaceDividendsParse(object):

    def __init__(self, page_source):
        self.race_date = ''
        self.dividend_dict = {}  # race_No & []
        self.__parse(page_source)

    def __parse(self, page_source):
        html = etree.HTML(page_source)

        # race info
        race_date_div = html.xpath('//td[@class="tdAlignL number13 color_black"]')
        race_date_text = race_date_div[0].xpath('string(.)')
        array_date = race_date_text.split(':')[1].split('/')
        self.race_date = array_date[2].strip() + array_date[1].strip() + array_date[0].strip()
        print('race_date:', self.race_date)

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
        # for race_no, array in self.dividend_dict.items():
        #     print('\nrace_no=', race_no)
        #     for item in array:
        #         print(item)

