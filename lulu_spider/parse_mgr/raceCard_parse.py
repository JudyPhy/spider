from parse_mgr import parseNote
from lxml import etree
import datetime

class RaceCard_Parse(parseNote.ParseBase):

    _tableLabel = 'draggable hiddenable'

    def getUrl(self,race_date):
        url = 'https://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/{}'.format(race_date)
        return url

    def getOtherUrls(self,page_source):
        html = etree.HTML(page_source)
        _urlList = html.xpath('//div[@class="raceNum clearfix"]//td//a/@href')

        return _urlList[:-1]

    def parse_sole_info(self,page_source):
        try:
            html = etree.HTML(page_source)
            race_info = html.xpath('//table[@class="font13 lineH20 tdAlignL"]')[0]

            tempTitle = race_info.xpath('.//span[@class="bold"]')
            tempInfo = race_info.xpath('.//br')

            title_list = tempTitle[0].text.replace('\xa0','').split("-")
            time_list = tempInfo[0].tail.replace('\r','').replace('\n','').replace(' ','').split(",")
            track_list = tempInfo[1].tail.replace('\r','').replace('\n','').replace(' ','').split(",")
            bonus_list = tempInfo[2].tail.replace('\r','').replace('\n','').split(", ")

            raceInfoDict = dict()

            raceInfoDict['raceNo'] = title_list[0].replace('Race ','')
            raceInfoDict['raceName'] = title_list[1]

            date_str = time_list[1]+','+time_list[2]
            raceInfoDict['raceDate'] = datetime.datetime.strptime(date_str,'%B%d,%Y').strftime('%Y%m%d')
            raceInfoDict['raceTime'] = time_list[4]
            raceInfoDict['raceSite'] = time_list[3]

            raceInfoDict['raceTrack'] = track_list[0]
            raceInfoDict['raceCourse'] = track_list[1].replace('Course','')
            raceInfoDict['raceDistance'] = track_list[2].replace('M','')

            raceInfoDict['raceBonus'] = bonus_list[0].replace('Prize Money: $','').replace(',','')
            raceInfoDict['raceRate'] = bonus_list[1].replace('Rating:','')
            raceInfoDict['raceCls'] = bonus_list[2].replace(' ','')

            return raceInfoDict
        except IndexError:
            print('RaceCard_Parse: parse_sole_info error!')
            return
