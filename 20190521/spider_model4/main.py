from spiders.race_results_spider import RaceResultsSpider
from spiders.horse_race_spider import HorseRaceSpider
from spiders.horse_pedigree_spider import HorsePedigreeSpider
from spiders.display_sectional_time_spider import DisplaySectionalTimeSpider
from spiders.race_card_spider import RaceCardSpider
from spiders.race_dividend_spider import RaceDividendSpider
from chromeDriver import singleton_chrome


def main():
    from_date = '2019-6-12'
    to_date = '2019-6-12'

    # print('RaceResultsSpider=>')
    # spider_raceResults = RaceResultsSpider()
    # spider_raceResults.setParams(from_date, to_date, True)  # setParams(from_date, to_date, rmLoaded)
    # spider_raceResults.spider_start()
    #
    # print('\n\nHorseRaceSpider=>')
    # spider_horseRace = HorseRaceSpider()
    # spider_horseRace.setParams(from_date, to_date, False)  # setParams(from_date, to_date, rmLoaded)
    # spider_horseRace.spider_start()
    #
    # print('\n\nHorsePedigreeSpider=>')
    # spider_horsePedigree = HorsePedigreeSpider()
    # spider_horsePedigree.setParams('2014-0-0', to_date, True)  # setParams(from_date, to_date, rmLoaded)
    # spider_horsePedigree.spider_start()
    #
    # print('\n\nDisplaySectionalTimeSpider=>')
    # spider_sectionalTime = DisplaySectionalTimeSpider()
    # spider_sectionalTime.setParams(from_date, to_date, True)  # setParams(from_date, to_date, rmLoaded)
    # spider_sectionalTime.spider_start()

    print('\n\nRaceCardSpider=>')
    spider_raceCard = RaceCardSpider()
    spider_raceCard.setParams(from_date, to_date, False)  # setParams(from_date, to_date, rmLoaded)
    spider_raceCard.spider_start()

    # print('\n\nRaceDividend=>')
    # spider_dividend = RaceDividendSpider()
    # spider_dividend.setParams(from_date, to_date, True)  # setParams(from_date, to_date, rmLoaded)
    # spider_dividend.spider_start()


if __name__ == '__main__':
    main()
    singleton_chrome.driver.close()
    singleton_chrome.driver.quit()

