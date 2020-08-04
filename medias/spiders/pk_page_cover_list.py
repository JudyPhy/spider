from chromeDriver import singleton_chrome
import time
from lxml import etree
from spiders.pk_page_detail_info import pk_page_detail_info


class pk_page_cover_list(object):

    base_url = 'https://www.pianku.tv/'

    def __init__(self, ex):
        url = self.base_url + ex
        print('request=>', url)
        singleton_chrome.driver.get(url)
        time.sleep(1)
        # print(singleton_chrome.driver.page_source)
        self.__parse_page()

    def __parse_page(self):
        medias = singleton_chrome.driver.find_elements_by_xpath('//ul[@class="content-list"]/li')
        for li in medias[15:16]:
            # print(li.text)
            cover = li.find_element_by_xpath('./div[@class="li-img cover"]')
            data_id = cover.get_attribute('data-id')
            info = cover.find_element_by_xpath('./a')
            detail_url = info.get_attribute('href')
            title = info.get_attribute('title')
            img = info.find_element_by_xpath('./img')
            img_src = img.get_attribute('src')
            bottom_info = li.find_element_by_xpath('./div[@class="li-bottom"]')
            span = bottom_info.find_element_by_xpath('./h3/span')
            score = span.text
            tag = bottom_info.find_element_by_xpath('./div[@class="tag"]').text
            # print('data_id:', data_id, '\ndetail_url:', detail_url, '\ntitle:', title, '\nimg_src:',
            #       img_src, '\nscore:', score, '\ntag:', tag)
            pk_page_detail_info(detail_url)

        return
        div_pages = singleton_chrome.driver.find_element_by_xpath('//div[@class="pages"]')
        cur_page_index = int(div_pages.find_element_by_xpath('./span').text)
        pages = div_pages.find_elements_by_xpath('./a')
        next_page_index = 0
        for a in pages:
            index = a.text.replace('.', '')
            if index == '上一页' or index == '下一页':
                continue
            if int(index) > cur_page_index:
                next_page_index = index
                print('cur_page_index:', cur_page_index, ', next_page_index:', next_page_index)
                next_page_url = a.get_attribute('href')
                print('request=>', next_page_url)
                singleton_chrome.driver.get(next_page_url)
                time.sleep(1)
                self.__parse_page()
                break




