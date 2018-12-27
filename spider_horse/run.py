from race_horse import RaceHorseSpider
from url.urlManager import singleton as singleton_url
from config.myconfig import singleton as singleton_cfg
from common import common
import time
from chromeDriver import singleton_chrome


def main():
    while(True):
        if singleton_cfg.spiderLost():
            url_list = singleton_url.getLostUrlList()
        else:
            url_list = singleton_url.getUrlList()
        common.log('need spider url count=' + str(len(url_list)))
        if len(url_list) <= 0:
            singleton_chrome.quit()
            break
        else:
            RaceHorseSpider().start_requests(url_list)
            time.sleep(5)


if __name__ == '__main__':
    main()

