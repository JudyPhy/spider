from spider import firefox
from parse_mgr import urlDate_parse
from db import conn

spider_driver = firefox.spiderDriver
conn = conn.engine
urlParser = urlDate_parse.DateUrl_Parse()

url = 'https://racing.hkjc.com/racing/chinese/racing-info/newhorse.asp?racedate=20190414&raceNo=&brandNo='
page_source = spider_driver.spider_url(url)
horse_url_list = urlParser.parseHorseUrl(page_source)
print(horse_url_list[:3])


