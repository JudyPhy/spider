from ..config.myconfig import singleton_cfg
from ..common import common


class RaceCardParse(object):

    def __init__(self, response):
        # race info
        array_date = singleton_cfg.getRequestDay().split('-')
        self.race_date = str(array_date[0]) + common.toDoubleDigitStr(array_date[1]) + common.toDoubleDigitStr(array_date[2])
        self.race_time = ''
        self.race_id = 0
        self.race_No = 0
        self.site = ""
        self.cls = 0
        self.distance = 0
        self.bonus = 0
        self.going = ''
        self.course = ''

        self.table_card = []

        self.__parse(response)

    def __parseCardTable(self, response):
        tables_card = response.xpath('.//table[@class="draggable hiddenable"]')
        if len(tables_card) > 0:
            trs_card = tables_card[0].xpath('.//tr')
            for each_tr in trs_card:
                tds_row = each_tr.xpath('./td')
                if len(tds_row) == 25:
                    row = []
                    for each_td in tds_row:
                        image_block = each_td.xpath('./img/@alt')
                        if len(image_block) > 0:
                            block = image_block.extract()[0]
                        else:
                            block = each_td.xpath('string(.)').extract()[0]
                        row.append(block)
                    self.table_card.append(row)
                    # print('row:', row)
        pass

    def __parseRaceInfo(self, response):
        divs_info = response.xpath('.//div[@class="rowDiv10"]')
        if len(divs_info) > 0:
            tables = divs_info[0].xpath('.//table')
            if len(tables) > 0:
                tds = tables[0].xpath('.//td')
                if len(tds) > 0:
                    info_text = tds[0].xpath('string(.)').extract()[0]
                    array_info = info_text.split('\r\n')
                    if len(array_info) == 7:
                        # line1
                        array_line_1 = array_info[1].strip().split('\xa0')
                        if len(array_line_1) > 0:
                            self.race_No = int(array_line_1[0].replace('Race', ''))

                        # line2
                        array_line_2 = array_info[3].strip().split(',')
                        if len(array_line_2) == 5:
                            self.site = array_line_2[3]
                            self.race_time = array_line_2[4].strip()

                        # line3/4
                        array_line34 = array_info[5].strip().split('Prize Money:')
                        if len(array_line34) == 2:
                            # line3
                            array_line_3 = array_line34[0].split(',')
                            if 'Turf' in array_line_3[0]:
                                self.course = array_line_3[1].replace('Course', '').replace('"', '').strip()
                                self.distance = int(array_line_3[2].replace('M', ''))
                            else:
                                self.course = array_line_3[0].replace('Course', '').replace('"', '').strip()
                                self.distance = int(array_line_3[1].replace('M', ''))
                                self.going = array_line_3[2].strip().upper()

                            # line4
                            array_line_4 = array_line34[1].split('-')
                            if len(array_line_4) == 2:
                                array_bonus = array_line_4[0].split('Rating')
                                if len(array_bonus) > 0:
                                    self.bonus = int(array_bonus[0].replace(',', '').replace('$', ''))
                                array_cls = array_line_4[1].split(',')
                                if len(array_cls) > 0:
                                    self.cls = array_cls[len(array_cls) - 1]
        if self.race_No != 0:
            print('race info=> race_date:', self.race_date, ' race_time:', self.race_time, ' race_No:', self.race_No, ' site:', self.site,
                  ' course:', self.course, ' distance:', self.distance, ' bonus:', self.bonus)
        pass

    def __parse(self,response):
        self.__parseRaceInfo(response)
        self.__parseCardTable(response)



