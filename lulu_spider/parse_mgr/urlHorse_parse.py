from lxml import etree
import pandas as pd

class HorseUrl_Parse():

    def get_horseOrder_url(self,order):
        order_url = 'https://racing.hkjc.com/racing/information/English/Horse/SelectHorsebyChar.aspx?ordertype={}'.format(
            order)
        return order_url

    def parseHorseUrl(self,page_source):
        html = etree.HTML(page_source)

        url_list = html.xpath('//table[@class="bigborder"]//table//li//a')

        urlDict = dict()
        for url in url_list:
            urlDict[url.text] = 'https://racing.hkjc.com' + url.xpath('.//@href')[0]

        df = pd.DataFrame()
        df['horseName'] = list(urlDict)
        df['horseUrl'] = list(urlDict.values())

        if urlDict =={}:
            return None,None,False

        return urlDict,df,True