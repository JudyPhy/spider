from parse_mgr import parseNote
from lxml import etree

class RaceResult_Parse(parseNote.ParseBase):

    _tableLabel = 'f_tac table_bd draggable'

    def getUrl(self,race_date):
        url = 'https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate={}'.format(race_date)
        return url

    def getOtherUrls(self,page_source):
        html = etree.HTML(page_source)
        _urlList = html.xpath('//table[@class="f_fs12 f_fr js_racecard"]//td//a/@href')

        return _urlList[:-1]

    def parse_sole_info(self,page_source):
        try:
            html = etree.HTML(page_source)
            race_info = html.xpath('//div[@class="race_tab"]//table')[0]
            date_info = html.xpath('//div[@class="raceMeeting_select"]//p//span[@class="f_fl f_fs13"]')[0]

            tempTitle = race_info.xpath('.//tr[@class="bg_blue color_w font_wb"]//td')
            tempInfo = race_info.xpath('.//tbody[@class="f_fs13"]//tr')

            raceInfoDict = dict()
            date_list = date_info.text.replace('Race Meeting:','').replace('\xa0','').split(" ")
            raceInfoDict['raceDate'] = date_list[1]
            raceInfoDict['raceSite'] = date_list[-2]+date_list[-1]
            _, raceInfoDict['raceNo'], raceInfoDict['raceId'] = tempTitle[0].text.replace('(','').replace(')','').split(" ")

            #tr=0
            #tr=1
            tr1_list = tempInfo[1].xpath('.//td')
            track_list = tr1_list[0].text.split("M")
            raceInfoDict['raceCls'],raceInfoDict['raceDistance'] = track_list[0].replace(' ','').split("-")
            raceInfoDict['raceRate'] = ''
            if len(track_list)>1:
                raceInfoDict['raceRate'] = track_list[1].replace(')','').replace(' - (','')

            raceInfoDict['raceGo'] = tr1_list[2].text

            #tr=2
            tr2_list = tempInfo[2].xpath('.//td')
            raceInfoDict['raceName'] = tr2_list[0].text
            raceInfoDict['raceTrack'], raceInfoDict['raceCourse'] = tr2_list[2].text.replace(' ','').split("-")

            #tr=3
            tr3_list = tempInfo[3].xpath('.//td')
            raceInfoDict['raceBonus'] = tr3_list[0].text.replace('HK$ ','').replace(',','')
            raceInfoDict['raceTotalTime'] = tr3_list[-1].text.replace('(','').replace(')','')

            #tr=4
            tr4_list = tempInfo[4].xpath('.//td')
            raceInfoDict['raceEndTime'] = tr4_list[-1].text.replace('(', '').replace(')', '')

            print(raceInfoDict)

            return raceInfoDict
        except IndexError:
            print('RaceResult_Parse: parse_sole_info error!')
            return
