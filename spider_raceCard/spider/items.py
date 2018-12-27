# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RaceCardItem(scrapy.Item):
    race_date = scrapy.Field()
    race_time = scrapy.Field()
    race_id = scrapy.Field()
    race_No = scrapy.Field()
    site = scrapy.Field()
    cls = scrapy.Field()
    distance = scrapy.Field()
    bonus = scrapy.Field()
    course = scrapy.Field()
    going = scrapy.Field()

    horse_No = scrapy.Field()
    last_6_runs = scrapy.Field()
    horse = scrapy.Field()
    horse_code = scrapy.Field()
    wt = scrapy.Field()
    jockey = scrapy.Field()
    over_wt = scrapy.Field()
    draw = scrapy.Field()
    trainer = scrapy.Field()
    rtg = scrapy.Field()
    rtg_as = scrapy.Field()
    horse_wt_dec = scrapy.Field()
    wt_as_dec = scrapy.Field()
    best_time = scrapy.Field()
    age = scrapy.Field()
    wfa = scrapy.Field()
    sex = scrapy.Field()
    season_stacks = scrapy.Field()
    priority = scrapy.Field()
    gear = scrapy.Field()
    owner = scrapy.Field()
    sire = scrapy.Field()
    dam = scrapy.Field()
    import_cat = scrapy.Field()
