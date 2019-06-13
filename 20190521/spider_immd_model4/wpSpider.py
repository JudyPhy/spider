from common import common
from chromeDriver import singleton_chrome
import time
from lxml import etree


class WPSpider(object):

    def __init__(self, url):
        self.race_info = {}
        self.wpTable = {}
        self.__requests(url)
        pass

    def __requests(self, url):
        print('request=>', url)
        try:
            singleton_chrome.driver.get(url)
            time.sleep(0.2)
            self.__parsePage(singleton_chrome.driver.page_source)
            # self.__parseRaceInfo()
            # self.__parseWPTable(race_date, race_no)
        except Exception as error:
            common.log('parse page error:' + str(error))

    def __parsePage(self, page_source):
        html = etree.HTML(page_source)

        # race info
        info_tables = html.xpath('//table[@id="info_bar"][1]//table')
        info_tds = info_tables[4].xpath('.//td')
        self.race_info['race_No'] = int(info_tds[0].xpath('string(.)').replace('Race', ''))
        array_split_dst = info_tds[2].xpath('string(.)').split('0m')
        array_split_dst_0 = array_split_dst[0].split(',')
        array_date = array_split_dst_0[1].split('/')
        self.race_info['race_date'] = array_date[2].strip() + array_date[1].strip() + array_date[0].strip()
        self.race_info['start_time'] = array_split_dst_0[2].strip()
        self.race_info['cls'] = array_split_dst_0[3].strip()
        self.race_info['course'] = ''.join(array_split_dst_0[4: len(array_split_dst_0) - 1])
        array_split_dst_1 = array_split_dst[1].split(',')
        going = array_split_dst_1[len(array_split_dst_1) - 1].replace(' ', '').upper()
        if going == '':
            going = 'GOOD'
        self.race_info['going'] = going
        array_date_time_cls_course_dis_going = info_tds[2].xpath('string(.)').split(',')
        for text in array_date_time_cls_course_dis_going:
            if '0m' in text:
                self.race_info['distance'] = int(text.replace('m', ''))
                break
        print('race_info:', self.race_info)

        # wp table
        self.wpTable = {}    # horse_no & {key=>horse_name, draw, wt, jockey, trainer, win, place, win&place}
        wp_trs = html.xpath('//div[@id="detailWPTable"][1]//tr')
        for tr in wp_trs[1:]:
            tds = tr.xpath('./td')
            horse_No_text = tds[0].xpath('string(.)')
            if 'F' in horse_No_text:
                continue
            horse_No = int(horse_No_text)
            if horse_No not in self.wpTable.keys():
                info = {}
                horse_code_ele = tds[1].xpath('.//img')
                info['horse_code'] = horse_code_ele[0].attrib.get('title').strip()
                info['horse_name'] = tds[2].xpath('string(.)')
                if len(tds) == 10:
                    info['exit_race'] = False
                    draw = tds[3].xpath('string(.)')
                    if draw == '':
                        info['draw'] = 0
                    else:
                        info['draw'] = int(draw)
                    wt = tds[4].xpath('string(.)')
                    if wt == '':
                        info['wt'] = 0
                    else:
                        info['wt'] = int(wt)
                    info['jockey'] = tds[5].xpath('string(.)').strip()
                    info['trainer'] = tds[6].xpath('string(.)').strip()
                    info['win_odds'] = tds[7].xpath('string(.)')
                    info['pla_odds'] = tds[8].xpath('string(.)')
                    info['win_pla'] = tds[9].xpath('string(.)')
                    if ('SCR' in info['win_odds']) and ('SCR' in info['pla_odds']):
                        info['exit_race'] = True
                    self.wpTable[horse_No] = info
                else:
                    info['exit_race'] = True
                    info['draw'] = 0
                    info['wt'] = 0
                    info['jockey'] = ''
                    info['trainer'] = ''
                    info['win_odds'] = ''
                    info['pla_odds'] = ''
                    info['win_pla'] = ''

                # info = {}
                # info['exit_race'] = True
                # self.wpTable[horse_no] = info
        # for key, value in self.wpTable.items():
        #     print('wp', key, value)

