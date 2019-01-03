from chromeDriver import singleton_chrome
from common import common
import time


class HorseInfoParse(object):

    def __init__(self, url):
        self.parseOver = False
        self.horse_info = {}
        self.__temp_dict = {}
        self.__initHorseInfo()
        self.__parse(url)
        pass

    def __initHorseInfo(self):
        self.horse_info['name'] = ''
        self.horse_info['code'] = ''
        self.horse_info['retired'] = ''
        self.horse_info['country_of_origin'] = ''
        self.horse_info['age'] = 0
        self.horse_info['trainer'] = ''
        self.horse_info['color'] = ''
        self.horse_info['sex'] = ''
        self.horse_info['owner'] = ''
        self.horse_info['import_type'] = ''
        self.horse_info['current_rating'] = 0
        self.horse_info['season_stakes'] = 0
        self.horse_info['start_of_season_rating'] = 0
        self.horse_info['total_stakes'] = 0
        self.horse_info['sire'] = ''
        self.horse_info['No_1'] = 0
        self.horse_info['No_2'] = 0
        self.horse_info['No_3'] = 0
        self.horse_info['No_of_starts'] = 0
        self.horse_info['dam'] = ''
        self.horse_info['No_of_starts_in_past_10_race_meetings'] = ''
        self.horse_info['dams_sire'] = ''
        self.horse_info['current_location'] = ''
        self.horse_info['arrival_date'] = ''
        self.horse_info['same_sire'] = []
        self.horse_info['last_rating'] = ''
        pass

    def __parse(self, url):
        try:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            self.__parseHorseInfoPage(url)
        finally:
            pass

    def __getKeyValueList(self, element, needOption=False, isArrivalDate=False, isOwner=False):
        result = []
        if needOption:
            options = element.find_elements_by_xpath('.//option')
            if len(options) > 0:
                list = []
                for horse in options:
                    str_name = horse.text
                    list.append(str_name)
                result.append(list)
        else:
            if '/' in element.text and not isArrivalDate and not isOwner:
                array = element.text.split('/')
                for key in array:
                    result.append(key.strip())
            else:
                result.append(element.text)
        return result

    def __parseBlocks(self, tds):
        if len(tds) == 3:
            keys = self.__getKeyValueList(tds[0])
            needOption = 'Same Sire' in keys
            isArrivalDate = len(keys) > 0 and 'Arrival Date' in keys[0]
            isOwner = len(keys) == 1 and 'Owner' in keys[0]
            values = self.__getKeyValueList(tds[2], needOption, isArrivalDate, isOwner)
            if len(keys) == len(values):
                for index, key in enumerate(keys):
                    temp_key = key.replace(' ', '')
                    if len(temp_key) > 0:
                        self.__temp_dict[key] = values[index]
            else:
                print('key != value', keys, ' & ', values)
        else:
            print('block td length error')
        pass

    def __restructTempDict(self):
        for key in self.__temp_dict:
            if 'Country' in key:
                self.horse_info['country_of_origin'] = self.__temp_dict[key].replace(':', '').strip()
            if 'Age' in key:
                self.horse_info['age'] = self.__temp_dict[key].replace(':', '').strip()
            if 'Trainer' in key:
                self.horse_info['trainer'] = self.__temp_dict[key].replace(':', '')
            if 'Colour' in key:
                self.horse_info['color'] = self.__temp_dict[key].replace(':', '').strip()
            if 'Sex' in key:
                self.horse_info['sex'] = self.__temp_dict[key].replace(':', '').strip()
            if 'Owner' in key:
                self.horse_info['owner'] = self.__temp_dict[key].replace(':', '')
            if 'Import Type' in key:
                self.horse_info['import_type'] = self.__temp_dict[key].replace(':', '')
            if 'Current Rating' in key:
                self.horse_info['current_rating'] = self.__temp_dict[key].replace(':', '')
                if self.horse_info['current_rating'] == '':
                    self.horse_info['current_rating'] = 0
            if 'Season Stakes' in key:
                self.horse_info['season_stakes'] = self.__temp_dict[key].replace(':', '').replace('$','').replace(',', '')
            if 'Start of' in key and 'Season Rating' in key:
                self.horse_info['start_of_season_rating'] = self.__temp_dict[key].replace(':', '')
                if self.horse_info['start_of_season_rating'] == '':
                    self.horse_info['start_of_season_rating'] = 0
            if 'Total Stakes' in key:
                self.horse_info['total_stakes'] = self.__temp_dict[key].replace(':', '').replace('$','').replace(',', '')
            if key == 'Sire':
                self.horse_info['sire'] = self.__temp_dict[key].replace('\r\n', '').replace(':', '')
            if '1-2-3-Starts' in key:
                array_starts = self.__temp_dict[key].replace(':', '').split('-')
                if len(array_starts) == 4:
                    self.horse_info['No_1'] = array_starts[0]
                    self.horse_info['No_2'] = array_starts[1]
                    self.horse_info['No_3'] = array_starts[2]
                    self.horse_info['No_of_starts'] = array_starts[3]
                else:
                    pass
            if 'Dam' == key:
                self.horse_info['dam'] = self.__temp_dict[key].replace(':', '')
            if 'starts in past 10' in key:
                self.horse_info['No_of_starts_in_past_10_race_meetings'] = self.__temp_dict[key].replace(':', '')
            if "Dam's Sire" == key:
                self.horse_info['dams_sire'] = self.__temp_dict[key].replace(':', '')
            if "Location" in key:
                loc_and_totime = self.__temp_dict[key].replace(':', '')
                self.horse_info['current_location'] = loc_and_totime.split('(')[0].replace('\n', '')
                self.horse_info['arrival_date'] = loc_and_totime.split('(')[1].split(')')[0]
            if "Same Sire" in key:
                self.horse_info['same_sire'] = self.__temp_dict[key]
            if "Last Rating" in key:
                self.horse_info['last_rating'] = self.__temp_dict[key].replace(':', '')

            self.parseOver = True
        pass

    def __parseHorseInfoPage(self, url):
        try:
            ele_name = singleton_chrome.driver.find_element_by_xpath('.//td[@class="subsubheader"]')
            if ele_name:
                name = ele_name.text.replace('&nbsp;','')
                self.horse_info['retired'] = 'Retired' in name
                print('retired:', self.horse_info['retired'])
                temp_name = name.replace('(Retired)', '')
                if '(' in temp_name:
                    array_name = temp_name.split('(')
                    self.horse_info['name'] = array_name[0]
                    self.horse_info['code'] = array_name[len(array_name) - 1].replace(')', '')
                else:
                    self.horse_info['name'] = temp_name
                    self.horse_info['code'] = 0
                print('name:', self.horse_info['name'], ' code:', self.horse_info['code'])
            else:
                pass

            table_horse_profire = singleton_chrome.driver.find_elements_by_xpath('.//table[@class="horseProfile"]')
            if len(table_horse_profire) > 0:
                tables = table_horse_profire[0].find_elements_by_xpath('.//table')
                exTableCount = 0
                # 马匹图片table、骑手着衣table: 必须的2个table嵌套于一个大的父table中，该父table可能不止包含了这2个table，
                # 因此需要计算出其包含的table数量exTableCount，以确认马匹信息table的索引号
                if len(tables) > 0:
                    tables_1 = tables[0].find_elements_by_xpath('.//table')
                    exTableCount = len(tables_1)
                # 马匹信息分左右两个表显示
                if len(tables) > (1 + exTableCount):
                    table_left = tables[1 + exTableCount]
                    trs_left = table_left.find_elements_by_xpath('.//tr')
                    for tr_left in trs_left:
                        tds_left = tr_left.find_elements_by_xpath('./td')
                        self.__parseBlocks(tds_left)
                    self.__restructTempDict()
                if len(tables) > (2 + exTableCount):
                    table_right = tables[2 + exTableCount]
                    trs_right = table_right.find_elements_by_xpath('.//tr')
                    for tr_right in trs_right:
                        tds_right = tr_right.find_elements_by_xpath('./td')
                        self.__parseBlocks(tds_right)
                    self.__restructTempDict()
                else:
                    print('horse info table not exist')
        except Exception as error:
            common.log('chrome page error:' + url + '\n' + str(error))
        pass


