from parse_mgr import parseNote
from lxml import etree
import re

class Horse_Parse(parseNote.ParseBase):

    _tableLabel = 'bigborder'

    def getUrl(self,horseCode):
        url = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseNo={}&Option=1'.format(horseCode)
        return url

    def parse_sole_info(self, page_source):
        try:
            html = etree.HTML(page_source)
            name_span = html.xpath('//td[@class="subsubheader"]//span[@class="title_text"]')
            name_str = name_span[0].text.replace(' ', '')

            horseInfoDict = dict()
            horseInfoDict['doRetired'] = 'Retired' in name_str

            _tempName = name_str.replace('(Retired)', '')
            _horseCode = re.findall(r'[(](.*?)[)]',_tempName)[0]
            horseInfoDict['horseName'] = _tempName.replace('({})'.format(_horseCode), '')
            horseInfoDict['horseCode'] = _horseCode

            return horseInfoDict
        except IndexError:
            print('Horse_Parse: parse_sole_info error!')
            return