from spiders.pk_page_cover_list import pk_page_cover_list
from chromeDriver import singleton_chrome


def main():
    spider_pk_page_cover_list = pk_page_cover_list('mv')
    # spider_pk_page_cover_list = pk_page_cover_list('tv')
    # spider_pk_page_cover_list = pk_page_cover_list('ac')


if __name__ == '__main__':
    main()
    singleton_chrome.driver.close()
    singleton_chrome.driver.quit()