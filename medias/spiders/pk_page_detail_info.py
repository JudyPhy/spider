from chromeDriver import singleton_chrome
import time
from db.db import singleton_PKMediaDb
from common import common
from db import db_media_play_src


class pk_page_detail_info(object):

    def __init__(self):
        self.searchUrl()

    def searchUrl(self):
        tableName = common.POSTER_INFO_TABLE
        if singleton_PKMediaDb.table_exists(tableName):
            singleton_PKMediaDb.cursor.execute("select data_id,detail_url from {}".format(tableName))
            repetition = singleton_PKMediaDb.cursor.fetchall()
            singleton_PKMediaDb.connect.commit()
            if repetition:
                for row in repetition:
                    self.gotoDetailPage(row['data_id'], row['detail_url'])
        else:
            print('table[', tableName, '] not exist')

    def gotoDetailPage(self, data_id, detail_url):
        print('request=>', detail_url)
        singleton_chrome.driver.get(detail_url)
        time.sleep(5)
        # print(singleton_chrome.driver.page_source)
        self.__parse_page(data_id)

    def __parse_page(self, data_id):
        loading = singleton_chrome.driver.find_element_by_xpath('//div[@id="url"]')
        if self.isElementExist(loading, './div[@id="play"]'):
            online_play = loading.find_element_by_xpath('./div[@id="play"]')
            play_url_uls = online_play.find_elements_by_xpath('./div[@class="bd"]/ul')
            play_url_list = []
            for ul in play_url_uls:
                url_li = ul.find_elements_by_xpath('./li')
                for li in url_li:
                    url = li.find_element_by_xpath('./a').get_attribute('href')
                    play_url_list.append(url)
            # print(play_url_list)
            pk_page_player(play_url_list, data_id)

    def isElementExist(self, parent, path):
        try:
            parent.find_element_by_xpath(path)
            return True
        except:
            return False


class pk_page_player(object):

    def __init__(self, url_list, data_id):
        for url in url_list[0:1]:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(2)
            # print(singleton_chrome.driver.page_source)
            self.__parse_page(data_id)

    def __parse_page(self, data_id):
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
                if url_m3u8.find('.m3u8') != -1:
                    result = [data_id, url_m3u8]
                    db_media_play_src.exportToDb(result)



