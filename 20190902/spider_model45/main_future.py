from spiders.race_card_spider import RaceCardSpider
from chromeDriver import singleton_chrome


def main():
    from_date = '2019-9-15'
    to_date = '2019-9-15'

    print('\n\nRaceCardSpider=>')
    spider_raceCard = RaceCardSpider()
    spider_raceCard.setParams(from_date, to_date, True)  # setParams(from_date, to_date, rmLoaded)
    days = 2
    spider_raceCard.spider_start(days)  # 以今天开始算起，爬取days天的排位数据，比如今天是9月11日，days=2，则爬取9月11日和9月12日的比赛数据


if __name__ == '__main__':
    main()
    singleton_chrome.driver.close()
    singleton_chrome.driver.quit()

