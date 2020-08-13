from chromeDriver import singleton_chrome
import time
from db.db import singleton_PKMediaDb
from common import common
from db import db_media_play_src
from db import db_media_meta


class pk_page_detail_info(object):

    type = ''
    dataId = ''
    result = []

    def __init__(self, ex):
        self.type = ex
        self.__searchUrl()

    def __searchUrl(self):
        tableName = common.POSTER_INFO_TABLE + '_' + self.type
        if singleton_PKMediaDb.table_exists(tableName):
            singleton_PKMediaDb.cursor.execute("select data_id,detail_url from {}".format(tableName))
            repetition = singleton_PKMediaDb.cursor.fetchall()
            singleton_PKMediaDb.connect.commit()
            if repetition:
                for row in repetition[0:100]:    # mv:1000
                    self.__gotoDetailPage(row['data_id'], row['detail_url'])
        else:
            print('table[', tableName, '] not exist')

    def __gotoDetailPage(self, data_id, detail_url):
        self.dataId = data_id
        print('request=>', detail_url)
        singleton_chrome.driver.get(detail_url)
        time.sleep(5)
        self.__parse_page()

    def __parse_meta(self):
        cover = singleton_chrome.driver.find_element_by_xpath('//div[@class="img cover"]/img').get_attribute("src")
        media_meta = singleton_chrome.driver.find_element_by_xpath('//div[@class="main-ui-meta"]')
        title = media_meta.find_element_by_xpath('./h1').text
        divs_meta = media_meta.find_elements_by_xpath('./div')
        director = ''
        screenwriter = ''
        starring = ''
        type = ''
        area = ''
        language = ''
        release = ''
        length = ''
        other_name = ''
        score = ''
        for div in divs_meta:
            if self.isElementExist(div, './span'):
                text = div.text
                if text.find('导演') != -1:
                    director = text.split('：')[1]
                elif text.find('编剧') != -1:
                    screenwriter = text.split('：')[1]
                elif text.find('主演') != -1:
                    a_names = div.find_elements_by_xpath('.//a')
                    names = []
                    for a in a_names:
                        str_name = a.get_attribute("outerHTML")
                        index = str_name.find('</a>')
                        actor = ''
                        record = False
                        for ch in str_name[: index]:
                            if record:
                                actor += ch
                            if ch == '>':
                                record = True
                        if actor != '':
                            names.append(actor)
                    starring = ''
                    for name in names:
                        starring += name + '/'
                    starring = starring[: len(starring) - 1]
                elif text.find('类型') != -1:
                    type = text.split('：')[1]
                elif text.find('地区') != -1:
                    area = text.split('：')[1]
                elif text.find('语言') != -1:
                    language = text.split('：')[1]
                elif text.find('上映') != -1:
                    release = text.split('：')[1]
                elif text.find('片长') != -1:
                    length = text.split('：')[1]
                elif text.find('又名') != -1:
                    other_name = text.split('：')[1]
                elif text.find('评分') != -1:
                    score = text.split('：')[1].replace('\n', '')
        self.result = [self.dataId, cover, title, director, screenwriter, starring, type, area, language, release, length, other_name, score]
        # print('title:', title, ', \ndirector:', director, ', \nscreenwriter:', screenwriter, ', \nstarring:', starring,
        #       ', \ntype:', type, ', \narea:', area, ', language:', language, ', release:', release, ', length:', length,
        #       ', \nother_name:', other_name, ', \nscore:', score)

    def __parse_introduce(self):
        movie_introduce = singleton_chrome.driver.find_element_by_xpath('//div[@class="movie-introduce"]')
        if self.isElementExist(movie_introduce, './p[@class="sqjj_a"]'):
            p_text = movie_introduce.find_element_by_xpath('./p[@class="sqjj_a"]').get_attribute("outerHTML")
            index_span = p_text.find('<span')
            p_text = p_text[: index_span]
            introduce = ''
            record = False
            for ch in p_text:
                if record:
                    introduce += ch
                if ch == '>':
                    record = True
        else:
            introduce = movie_introduce.text
        introduce = introduce.replace('\n', '').strip()
        self.result.append(introduce)
        # print('introduce:', introduce)
        db_media_meta.exportToDb(self.type, self.result)

    def __parse_loading(self):
        loading = singleton_chrome.driver.find_element_by_xpath('//div[@id="url"]')
        if self.isElementExist(loading, './div[@id="play"]'):
            online_play = loading.find_element_by_xpath('./div[@id="play"]')
            play_url_uls = online_play.find_elements_by_xpath('./div[@class="bd"]/ul')
            play_url_list = []
            for ul in play_url_uls:  # 每个ul是一个播放源类型
                url_li = ul.find_elements_by_xpath('./li')
                cur_ul_urls = []
                for li in url_li:   # 每个li是一集/一种分辨率
                    url = li.find_element_by_xpath('./a').get_attribute('href')
                    text_a = li.find_element_by_xpath('./a').get_attribute('outerHTML')
                    index_a = text_a.find('>')
                    style = ''
                    for ch in text_a[index_a + 1:]:
                        if ch == '<':
                            break
                        style += ch
                    section = {}
                    section['type'] = style
                    section['url'] = url
                    cur_ul_urls.append(section)
                # print('cur_ul_urls:', cur_ul_urls)
                play_url_list.append(cur_ul_urls)
            pk_page_player(play_url_list, self.dataId, self.type)

    def __parse_page(self):
        if not self.__isLoadedToMeta():
            self.__parse_meta()
            self.__parse_introduce()
        if not self.__isLoadedToPlaySrc():
            self.__parse_loading()

    def isElementExist(self, parent, path):
        try:
            parent.find_element_by_xpath(path)
            return True
        except:
            return False

    def __isLoadedToMeta(self):
        tableName = common.MEDIA_META_TABLE + '_' + self.type
        if singleton_PKMediaDb.table_exists(tableName):
            singleton_PKMediaDb.cursor.execute("select data_id from {} where data_id=%s".format(tableName), self.dataId)
            repetition = singleton_PKMediaDb.cursor.fetchone()
            singleton_PKMediaDb.connect.commit()
            if repetition:
                return True
        return False

    def __isLoadedToPlaySrc(self):
        tableName = common.MEDIA_PLAY_SRC_TABLE + '_' + self.type
        if singleton_PKMediaDb.table_exists(tableName):
            singleton_PKMediaDb.cursor.execute("select data_id from {} where data_id=%s".format(tableName), self.dataId)
            repetition = singleton_PKMediaDb.cursor.fetchone()
            singleton_PKMediaDb.connect.commit()
            if repetition:
                return True
        return False


class pk_page_player(object):

    type = ''
    dataId = ''

    def __init__(self, url_list, data_id, ex):
        self.type = ex
        self.dataId = data_id
        result = [self.dataId]
        for cur_ul_urls in url_list:
            # 一种源类型
            cur_text = ''
            for item_url in cur_ul_urls:
                type = item_url['type']
                url = item_url['url']
                # print(type, ' request=>', url)
                singleton_chrome.driver.get(url)
                time.sleep(5)
                # print(singleton_chrome.driver.page_source)
                url_m3u8 = self.__parse_page()
                cur_text += 'type:' + type + ', ' + 'url:' + url_m3u8 + '\n'
            # print(cur_text)
            result.append(cur_text)
        # print(result)
        while (len(result) < 12):
            result.append('')
        db_media_play_src.exportToDb(self.type, result)

    def __parse_page(self):
        result = ''
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
                # print(url_m3u8)
                if url_m3u8.find('.m3u8') != -1:
                    result = url_m3u8
        return result



