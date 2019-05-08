from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class FireFoxDriver(webdriver.Firefox):

    _urlRoot = 'https://racing.hkjc.com'

    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument('--headless')

        webdriver.Firefox.__init__(self, firefox_profile=None, firefox_binary=None,
                 timeout=30, capabilities=None, proxy=None,
                 executable_path="geckodriver", options=None,
                 service_log_path="geckodriver.log", firefox_options=firefox_options,
                 service_args=None, desired_capabilities=None, log_path=None,
                 keep_alive=True)

        self.implicitly_wait(0)

    def spider_url(self,url):
        self.get(url)
        time.sleep(0.1)
        return self.page_source

    def spider_race(self, raceParse, url, homePage=False):
        if not homePage:
            url = self._urlRoot + url
        print(url)
        while True:
            page_source = self.spider_url(url)
            url_pd, err = raceParse.parse_page(page_source)

            if err:
                if homePage:
                    url_list = raceParse.getOtherUrls(page_source)
                    return url_pd, url_list
                return url_pd

    def spider_horse(self, horseParse, url):
        print(url)
        while True:
            page_source = self.spider_url(url)
            url_pd, err = horseParse.parse_page(page_source)

            if err:
                return url_pd

spiderDriver = FireFoxDriver()


