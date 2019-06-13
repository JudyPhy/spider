from chromeDriver import singleton_chrome
import time


class HorseInfoParse(object):

    def __init__(self, url):
        self.horse_info = {}
        self.__initHorseInfo()
        self.__parse(url)
        pass

    def __initHorseInfo(self):
        self.horse_info['name'] = ''
        self.horse_info['code'] = ''
        self.horse_info['grow'] = ''
        self.horse_info['distance'] = ''
        self.horse_info['track_affinity'] = ''
        pass

    def __parse(self, url):
        try:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.2)
            self.__parseHorseInfoPage(url)
        finally:
            pass

    def __parseHorseInfoPage(self, url):
        try:
            ele_name = singleton_chrome.driver.find_element_by_xpath('.//td[@class="table_title"]')
            if ele_name:
                name = ele_name.text
                if '(' in name:
                    array_name = name.strip().split('(')
                    self.horse_info['name'] = array_name[0]
                    self.horse_info['code'] = array_name[len(array_name) - 1].replace(')', '').strip()
                else:
                    self.horse_info['name'] = name
                    self.horse_info['code'] = 0
                print('name:', self.horse_info['name'], ' code:', self.horse_info['code'])
            else:
                pass

            divs_blood = singleton_chrome.driver.find_elements_by_xpath('.//div[@class="newhorse-txt"]')
            if len(divs_blood) > 2:
                div = divs_blood[2].text
                array = div.split('\n')
                for item in array:
                    if 'GROWTH' in item:
                        self.horse_info['grow'] = item.split(':')[1].strip()
                    elif 'DISTANCE' in item:
                        self.horse_info['distance'] = item.split(':')[1].strip()
                    elif 'TRACK AFFINITY' in item:
                        self.horse_info['track_affinity'] = item.split(':')[1].strip().replace('，', ',')
                print(self.horse_info['grow'], ',', self.horse_info['distance'], ',', self.horse_info['track_affinity'])
        except Exception as error:
            print('chrome page error:' + url + '\n' + str(error))
        pass


