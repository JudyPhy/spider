from horse_parse import HorseInfoParse
from db import db_horse


class RaceHorseSpider(object):

    def start_requests(self, url_list):
        for url in url_list:
            horse_parse = HorseInfoParse(url)
            self.exportToTable(horse_parse)

    def __getItem(self, info):
        item_horse = {}
        item_horse['name'] = info['name']
        item_horse['code'] = info['code']
        item_horse['retired'] = info['retired']
        item_horse['country_of_origin'] = info['country_of_origin']
        item_horse['age'] = info['age']
        item_horse['trainer'] = info['trainer']
        item_horse['color'] = info['color']
        item_horse['sex'] = info['sex']
        # owner may be too long
        str_owner = ''
        array_owner = info['owner'].split(',')
        for oneOwner in array_owner:
            str_owner += oneOwner.strip() + '|'
        if str_owner[len(str_owner) - 1] == '|':
            item_horse['owner'] = str_owner[:len(str_owner) - 1]
        else:
            item_horse['owner'] = str_owner

        item_horse['import_type'] = info['import_type']
        item_horse['current_rating'] = info['current_rating']
        item_horse['season_stakes'] = info['season_stakes']
        item_horse['start_of_season_rating'] = info['start_of_season_rating']
        item_horse['total_stakes'] = info['total_stakes']
        item_horse['sire'] = info['sire']
        item_horse['No_1'] = info['No_1']
        item_horse['No_2'] = info['No_2']
        item_horse['No_3'] = info['No_3']
        item_horse['No_of_starts'] = info['No_of_starts']
        item_horse['dam'] = info['dam']
        # No_of_starts_in_past_10_race_meetings
        item_horse['No_of_starts_in_past_10_race_meetings'] = info['No_of_starts_in_past_10_race_meetings']
        if info['No_of_starts_in_past_10_race_meetings'] == '':
            item_horse['No_of_starts_in_past_10_race_meetings'] = '0'

        item_horse['dams_sire'] = info['dams_sire']
        item_horse['current_location'] = info['current_location']
        item_horse['arrival_date'] = info['arrival_date']
        # same_sire
        item_horse['same_sire'] = ''
        for horse in info['same_sire']:
            item_horse['same_sire'] += horse + '|'

        item_horse['last_rating'] = info['last_rating']
        return item_horse

    def exportToTable(self, horse_parse):
        if horse_parse.parseOver:
            item = self.__getItem(horse_parse.horse_info)
            # print(item)
            db_horse.process_HorseInfoItem(item)
        else:
            print("can't export")