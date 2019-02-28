import scrapy
from scrapy.http import Request
from ..spiders.race_card_parse import RaceCardParse
from ..items import RaceCardItem
from ..url.urlManager import singleton_url


class raceCardURLSpider(scrapy.Spider):

    name = 'raceCard'
    allowed_domains = ['http://racing.hkjc.com']

    def start_requests(self):
        urlList = singleton_url.getHistoryUrlList()
        # urlList = singleton_url.getFutureUrlList()
        print('need spider url count:', len(urlList))
        for url in urlList:
            print('request=>', url)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        raceCard = RaceCardParse(response)
        for one in raceCard.table_card[1:]:
            if one[0] == 0:
                continue
            item_rank = RaceCardItem()
            item_rank['race_date'] = raceCard.race_date
            item_rank['race_time'] = raceCard.race_time
            item_rank['race_id'] = raceCard.race_id
            item_rank['race_No'] = raceCard.race_No
            item_rank['site'] = raceCard.site
            item_rank['cls'] = raceCard.cls
            item_rank['distance'] = raceCard.distance
            item_rank['bonus'] = raceCard.bonus
            item_rank['course'] = raceCard.course
            item_rank['going'] = raceCard.going
            item_rank['horse_No'] = one[0]
            item_rank['last_6_runs'] = one[1]
            item_rank['horse'] = one[3].replace('\r\n', '').strip()
            item_rank['horse_code'] = one[4]
            item_rank['wt'] = one[5]
            item_rank['jockey'] = one[6].replace('\r\n', '').strip()
            item_rank['over_wt'] = one[7].replace('\xa0', '').strip()
            item_rank['draw'] = one[8]
            item_rank['trainer'] = one[9].replace('\r\n', '').strip()
            item_rank['rtg'] = one[10]
            item_rank['rtg_as'] = one[11]
            item_rank['horse_wt_dec'] = one[12]
            item_rank['wt_as_dec'] = one[13]
            item_rank['best_time'] = one[14].replace('\xa0', '').strip()
            item_rank['age'] = one[15]
            item_rank['wfa'] = one[16]
            item_rank['sex'] = one[17]
            item_rank['season_stacks'] = one[18]
            item_rank['priority'] = one[19].replace('\r\n', '').strip()
            item_rank['gear'] = one[20].replace('\xa0', '').strip()
            item_rank['owner'] = one[21].strip()
            item_rank['sire'] = one[22].strip()
            item_rank['dam'] = one[23]
            item_rank['import_cat'] = one[24]
            yield item_rank