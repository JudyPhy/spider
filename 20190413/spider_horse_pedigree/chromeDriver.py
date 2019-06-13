import sys
sys.path.append("C:/Users/Rock/Anaconda3/Lib/site-packages")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeDriver(object):

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(0)

    def quit(self):
        self.driver.quit()


singleton_chrome = ChromeDriver()