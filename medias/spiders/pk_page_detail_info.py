from chromeDriver import singleton_chrome
import time
from lxml import etree
import re


class pk_page_detail_info(object):

    base_url = 'https://www.pianku.tv/'

    def __init__(self, detail_url):
        print('request=>', detail_url)
        singleton_chrome.driver.get(detail_url)
        time.sleep(5)
        # print(singleton_chrome.driver.page_source)
        self.__parse_page()

    def __parse_page(self):
        loading = singleton_chrome.driver.find_element_by_xpath('//div[@id="url"]')
        online_play = loading.find_element_by_xpath('./div[@id="play"]')
        play_url_uls = online_play.find_elements_by_xpath('./div[@class="bd"]/ul')
        play_url_list = []
        for ul in play_url_uls:
            url_li = ul.find_elements_by_xpath('./li')
            for li in url_li:
                url = li.find_element_by_xpath('./a').get_attribute('href')
                play_url_list.append(url)
        # print(play_url_list)
        pk_page_player(play_url_list)


class pk_page_player(object):

    def __init__(self, url_list):
        for url in url_list[0:1]:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(2)
            # print(singleton_chrome.driver.page_source)
            self.__parse_page()

    def __parse_page(self):
        scripts = singleton_chrome.driver.find_elements_by_xpath('//body//script')
        for script in scripts:
            outerHTML = script.get_attribute("outerHTML")
            index = outerHTML.find('geturl(')
            if index != -1:
                str = ''
                for ch in outerHTML[index:]:
                    str += ch
                    if ch == ')':
                        break
                url_m3u8 = str.replace('geturl(', '')
                url_m3u8 = url_m3u8[1:len(url_m3u8)-2]
                print(url_m3u8)



