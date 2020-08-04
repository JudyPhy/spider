from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_chrome


class ChromeDriver(object):

    def __init__(self):
        options = Options_chrome()
        # options.add_argument('--proxy-server=https://103.76.175.87:8080')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-cache')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(2)

    def __del__(self):
        pass


singleton_chrome = ChromeDriver()

