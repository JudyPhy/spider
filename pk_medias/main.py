from spiders.pk_page_detail_info import pk_page_detail_info
from chromeDriver import singleton_chrome


def main():
    # pk_page_detail_info('mv')
    # pk_page_detail_info('tv')
    pk_page_detail_info('ac')


if __name__ == '__main__':
    main()
    singleton_chrome.driver.close()
    singleton_chrome.driver.quit()

