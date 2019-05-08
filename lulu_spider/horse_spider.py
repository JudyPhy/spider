from spider import firefox
from parse_mgr import horseData_parse
from db import conn

spider_driver = firefox.spiderDriver
horseParse = horseData_parse.Horse_Parse()
conn = conn.engine


hcode_list = ['A277', 'B136']

for hcode in hcode_list:
    url = horseParse.getUrl(hcode)

    data_df = spider_driver.spider_horse(horseParse,url)
    print(data_df.head(1))
