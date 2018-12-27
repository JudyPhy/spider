import scrapy
from scrapy.http import Request
from ..spiders.race_results_parse import RaceResultsParse
from ..items import RaceResultsRankItem
from ..items import RaceResultsPayoutItem
from ..url.urlManager import singleton as singleton_url


class RaceResultsURLSpider(scrapy.Spider):

    name = 'raceResults'
    allowed_domains = ['http://racing.hkjc.com']

    def start_requests(self):
        urlList = singleton_url.getUrlList()
        for url in urlList:
            print('request=>', url)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        raceResults = RaceResultsParse(response)
        #print('raceResults count:',len(raceResults.table_rank_result))
        WV_index = 1000
        for one in raceResults.table_rank_result:
            item_rank = RaceResultsRankItem()
            item_rank['race_date'] = raceResults.race_date
            item_rank['race_id'] = raceResults.race_id
            item_rank['race_No'] = raceResults.race_No
            item_rank['site'] = raceResults.site
            item_rank['cls'] = raceResults.cls
            item_rank['distance'] = raceResults.distance
            item_rank['bonus'] = raceResults.bonus
            if raceResults.bonus == '':
                item_rank['bonus'] = 0
            item_rank['course'] = raceResults.course
            item_rank['going'] = raceResults.going
            item_rank['plc'] = one[0]
            item_rank['horse_No'] = one[1]
            if one[1] == '':
                item_rank['horse_No'] = str(WV_index)
                WV_index += 1

            if '(' in one[2]:
                array_horse = one[2].split('(')
                name = ''
                for i, value in enumerate(array_horse):
                    if i < (len(array_horse) - 1):
                        name = name + value + '('
                item_rank['horse'] = name[:len(name) - 1]
                item_rank['horse_code'] = array_horse[len(array_horse) - 1].replace(')', '').strip()
            else:
                item_rank['horse'] = one[2]
                item_rank['horse_code'] = 0

            item_rank['jockey'] = one[3]
            item_rank['trainer'] = one[4]

            if '-' in one[5]:
                item_rank['actual_wt'] = 0
            else:
                item_rank['actual_wt'] = one[5]

            item_rank['declar_horse_wt'] = one[6]
            item_rank['draw'] = one[7]
            item_rank['lbw'] = one[8]
            item_rank['running_position'] = one[9]
            item_rank['finish_time'] = one[10]

            if '-' in one[11]:
                item_rank['win_odds'] = 0
            else:
                item_rank['win_odds'] = one[11]
            yield item_rank

        for one in raceResults.table_payout:
            item_pay = RaceResultsPayoutItem()
            item_pay['race_date'] = raceResults.race_date
            item_pay['race_id'] = raceResults.race_id

            item_pay['pool'] = one['pool']
            item_pay['winning_combination'] = ''
            for comb in one['winning_combination']:
                item_pay['winning_combination'] += comb + '|'
            #print('winning_combination:', item_pay['winning_combination'])
            item_pay['dividend'] = ''
            for d in one['dividend']:
                item_pay['dividend'] += d + '|'
            #print('dividend:', item_pay['dividend'])

            yield item_pay

        #print('horse_urls count:',len(raceResults.horse_urls))