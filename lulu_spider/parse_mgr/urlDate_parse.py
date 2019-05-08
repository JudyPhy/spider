from lxml import etree

class DateUrl_Parse():

    url = 'https://racing.hkjc.com/racing/english/racing-info/newhorse.asp?racedate=20160101&raceNo=7&brandNo=V119'

    def parseHorseUrl(self,page_source):
        html = etree.HTML(page_source)

        url_list = html.xpath('//div[@class="droplist right"]//select[@id="raceDate"]//option//text()')

        return url_list[1:]