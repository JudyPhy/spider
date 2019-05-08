from spider import firefox
from parse_mgr import raceResult_parse,raceCard_parse
from db import conn
import datetime

spider_driver = firefox.spiderDriver
conn = conn.engine
#raceParse = raceResult_parse.RaceResult_Parse()
raceParse = raceCard_parse.RaceCard_Parse()

date_list = ['2019/04/14', '2019/04/10']

for date in date_list:
    date = datetime.datetime.strptime(date, '%Y/%m/%d').strftime('%Y%m%d')
    url = raceParse.getUrl(date)

    data_df,url_list = spider_driver.spider_race(raceParse=raceParse, url=url, homePage=True)
    print(data_df.head(1))

    for url_one in url_list:
        data2_df = spider_driver.spider_race(raceParse=raceParse, url=url_one, homePage=False)
        print(data2_df.head(1))