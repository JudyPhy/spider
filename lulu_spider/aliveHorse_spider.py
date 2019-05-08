from spider import firefox
from parse_mgr import urlHorse_parse
from db import conn

spider_driver = firefox.spiderDriver
conn = conn.engine
urlParser = urlHorse_parse.HorseUrl_Parse()


order_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
              'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def spiderByOrder(order):
    url = urlParser.get_horseOrder_url(order)
    while True:
        page_source = spider_driver.spider_url(url)
        _,url_pd,err = urlParser.parseHorseUrl(page_source)

        if err:
            #url_pd.to_sql("horse_url",con=conn,index=False,if_exists='append')
            print('order "{}" sipder data_num={} !'.format(order,len(url_pd)))
            break

for order in order_list:
    spiderByOrder(order)


