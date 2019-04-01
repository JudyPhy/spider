from race_results_parse import RaceResultsParse
from url.urlManager import singleton as singleton_url
from db import raceResults


class RaceResultsSpider(object):

    def __getItem(self, raceResults, row):
        WV_index = 1000
        race_date = raceResults.race_date
        race_id = raceResults.race_id
        race_No = raceResults.race_No
        site = raceResults.site
        cls = raceResults.cls
        distance = raceResults.distance
        bonus = raceResults.bonus
        if raceResults.bonus == '':
            bonus = 0
        course = raceResults.course
        going = raceResults.going

        plc = row[0]
        horse_No = row[1]
        if row[1] == '':
            horse_No = str(WV_index)
            WV_index += 1

        if '(' in row[2]:
            array_horse = row[2].split('(')
            name = ''
            for i, value in enumerate(array_horse):
                if i < (len(array_horse) - 1):
                    name = name + value + '('
            horse = name[:len(name) - 1]
            horse_code = array_horse[len(array_horse) - 1].replace(')', '').strip()
        else:
            horse = row[2]
            horse_code = 0

        jockey = row[3]
        trainer = row[4]

        if '-' in row[5]:
            actual_wt = 0
        else:
            actual_wt = row[5]

        declar_horse_wt = row[6]
        draw = row[7]
        lbw = row[8]
        running_position = row[9]
        finish_time = row[10]

        if '-' in row[11]:
            win_odds = 0
        else:
            win_odds = row[11]
        return (race_date, race_id, race_No, site, cls, distance, bonus, course, going, plc, horse_No, horse, horse_code,
                jockey, trainer, actual_wt, declar_horse_wt, draw, lbw, running_position, finish_time, win_odds)


    def start_requests(self):
        urlList = singleton_url.getUrlList()
        for url in urlList:
            rank_info = RaceResultsParse(url)
            if len(rank_info.table_rank_result) > 0:
                all_list = []
                for row in rank_info.table_rank_result:
                    item = self.__getItem(rank_info, row)
                    all_list.append(item)
                raceResults.exportRank(rank_info.race_date, rank_info.race_id, all_list)
