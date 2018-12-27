# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RaceResultsRankItem(scrapy.Item):
    race_date = scrapy.Field()
    race_id = scrapy.Field()
    race_No = scrapy.Field()
    site = scrapy.Field()
    cls = scrapy.Field()
    distance = scrapy.Field()
    bonus = scrapy.Field()
    course = scrapy.Field()
    going = scrapy.Field()

    plc = scrapy.Field()
    horse_No = scrapy.Field()
    horse = scrapy.Field()
    horse_code = scrapy.Field()
    jockey = scrapy.Field()
    trainer = scrapy.Field()
    actual_wt = scrapy.Field()
    declar_horse_wt = scrapy.Field()
    draw = scrapy.Field()
    lbw = scrapy.Field()
    running_position = scrapy.Field()
    finish_time = scrapy.Field()
    win_odds = scrapy.Field()

class RaceResultsPayoutItem(scrapy.Item):
    race_date = scrapy.Field()
    race_id = scrapy.Field()
    pool = scrapy.Field()
    winning_combination = scrapy.Field()
    dividend = scrapy.Field()

class HorseInfoItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    retired = scrapy.Field()
    country_of_origin = scrapy.Field()
    age = scrapy.Field()
    trainer = scrapy.Field()
    color = scrapy.Field()
    sex = scrapy.Field()
    owner = scrapy.Field()
    import_type = scrapy.Field()
    current_rating = scrapy.Field()
    season_stakes = scrapy.Field()
    start_of_season_rating = scrapy.Field()
    total_stakes = scrapy.Field()
    sire = scrapy.Field()
    No_1 = scrapy.Field()
    No_2 = scrapy.Field()
    No_3 = scrapy.Field()
    No_of_starts = scrapy.Field()
    dam = scrapy.Field()
    No_of_starts_in_past_10_race_meetings = scrapy.Field()
    dams_sire = scrapy.Field()
    same_sire = scrapy.Field()
    current_location = scrapy.Field()
    arrival_date = scrapy.Field()
    last_rating = scrapy.Field()
