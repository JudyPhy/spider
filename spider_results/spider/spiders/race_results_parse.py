class RaceResultsParse(object):

    def __init__(self, response):
        # race info
        self.race_date = ''
        self.race_id = 0
        self.race_No = 0
        self.site = ""
        self.cls = 0
        self.distance = 0
        self.bonus = 0
        self.going = ''
        self.course = ''

        self.table_rank_result = []
        self.table_payout = []
        self.winHorseInfo = {}

        self.__parse(response)

    def __parseRankTable(self, response):
        body = response.xpath('//tbody')
        if len(body)>0:
            trs = body[0].xpath('./tr')
            for each_tr in trs:
                tds = each_tr.xpath('./td')
                if len(tds) == 12:
                    row = []
                    for each_td in tds:
                        table_block = each_td.xpath('./table')
                        if len(table_block)>0:
                            td_pos = table_block.xpath('.//td')
                            block = ''
                            for pos in td_pos:
                                block += pos.xpath('string(.)').extract()[0] + ','
                            row.append(block)
                        else:
                            block = each_td.xpath('string(.)').extract()[0]
                            row.append(block)
                    self.table_rank_result.append(row)
        else:
            pass

    def __parseRaceInfo(self, response):
        td_site = response.xpath('.//td[@class="tdAlignL number13 color_black"]')
        if len(td_site)>0:
            text = td_site[0].xpath('string(.)').extract()[0].replace('\r\n','').replace(' ','')
            texts = text.split('\xa0')
            text_date = texts[0].split(':')
            if len(text_date)>1:
                self.race_date = text_date[1]
            else:
                self.race_date = texts[0]
            self.site = texts[len(texts) - 1]
            # print('race_date:', self.race_date, ' site:', self.site)
        else:
            pass

        wholedivs = response.xpath('.//div[@class="boldFont14 color_white trBgBlue"]')
        if len(wholedivs)>0:
            text = wholedivs[0].xpath('string(.)').extract()[0]
            if ('(' in text) and (')' in text):
                self.race_id = text.split('(')[1].split(')')[0]
                temp = text.split('(')[0].replace(' ','').replace('RACE','')
                self.race_No = temp
            else:
                pass
            # print('race_id:', self.race_id,' race_No:', self.race_No)
        else:
            pass

        table = response.xpath('.//table[@class="tableBorder0 font13"]')
        if len(table)>0:
            text_cls = table.xpath('./tr[1]/td[1]')
            if len(text_cls)>0:
                temp = text_cls[0].xpath('string(.)').extract()[0]
                if '-' in temp:
                    temp_array = temp.split('-')
                    self.cls = temp_array[0].replace(' ','')
                    temp_distance = temp_array[1].replace(' ','')
                    self.distance = temp_distance[:len(temp_distance)-1]
                    # print('cls:',self.cls, '  distance:',self.distance)
                else:
                    pass
            else:
                pass

            text_bonus = table.xpath('./tr[3]/td[1]')
            if len(text_bonus)>0:
                temp = text_bonus[0].xpath('string(.)').extract()[0]
                if ' ' in temp:
                    self.bonus = temp.split(' ')[1].replace(' ','').replace(',','')
                # print('bonus:', self.bonus)
            else:
                pass

            text_going = table.xpath('./tr[1]/td[3]')
            if len(text_going)>0:
                self.going = text_going[0].xpath('string(.)').extract()[0]
                # print('going:', self.going)
            else:
                pass

            text_course = table.xpath('./tr[2]/td[3]')
            if len(text_course)>0:
                self.course = text_course[0].xpath('string(.)').extract()[0]
                # print('course:', self.course)
            else:
                pass
        else:
            pass
    pass

    def __parsePayout(self,response):
        table = response.xpath('.//table[@class="tableBorder trBgBlue tdAlignC font13 fontStyle"]')
        if len(table)>0:
            trs = table[0].xpath('./tr')[2:]
            cur_pool = ''
            for tr in trs:
                row = {}
                tds = tr.xpath('./td')
                if len(tds) == 3:
                    cur_pool = tds[0].xpath('string(.)').extract()[0]
                    row['pool'] = cur_pool
                    row['winning_combination'] = []
                    row['winning_combination'].append(tds[1].xpath('string(.)').extract()[0])
                    row['dividend'] = []
                    row['dividend'].append(tds[2].xpath('string(.)').extract()[0])
                    self.table_payout.append(row)

                elif len(tds) == 2:
                    find = False
                    for pool in self.table_payout:
                        if pool['pool'] == cur_pool:
                            find = True
                            pool['winning_combination'].append(tds[0].xpath('string(.)').extract()[0])
                            pool['dividend'].append(tds[1].xpath('string(.)').extract()[0])
                    if not find:
                        row['pool'] = cur_pool
                        row['winning_combination'] = []
                        row['winning_combination'].append(tds[0].xpath('string(.)').extract()[0])
                        row['dividend'] = []
                        row['dividend'].append(tds[1].xpath('string(.)').extract()[0])
                        self.table_payout.append(row)
        else:
            pass

    def __parseWinHorseInfo(self,response):
        table = response.xpath('.//table[@class="trBgGrey3"]')
        if len(table)>0:
            trs = table[0].xpath('./tr')
            if len(trs)>2:
                tds = trs[2].xpath('./td')
                if len(tds)>1:
                    self.winHorseInfo['win_horse_name'] = tds[0].xpath('string(.)').extract()[0].replace(' ','')
                    str_info = tds[1].xpath('string(.)').extract()[0].replace(' ','')
                    strs = str_info.split('\r\n')
                    self.winHorseInfo['sire'] = strs[2].split(':')[1]
                    self.winHorseInfo['dam'] = strs[4].split(':')[1]
                else:
                    pass
            else:
                pass
        else:
            pass

    def __parse(self,response):
        self.__parseRaceInfo(response)
        self.__parseRankTable(response)
        self.__parsePayout(response)
        self.__parseWinHorseInfo(response)



