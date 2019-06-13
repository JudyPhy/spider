from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeDriver(object):

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--proxy-server=socks5://192.168.28.5:1')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(0)

    def quit(self):
        self.driver.quit()


singleton_chrome = ChromeDriver()