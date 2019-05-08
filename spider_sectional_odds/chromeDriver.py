from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_chrome


class ChromeDriver(object):

    def __init__(self):
        options = Options_chrome()
        # options.add_argument('--proxy-server=socks5://192.168.28.5:1')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(0)

    def __del__(self):
        pass
        # self.driver.close()
        # self.driver.quit()


singleton_chrome = ChromeDriver()

