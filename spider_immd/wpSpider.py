from common import common
from db.db import singleton_ResultsDb
from db.db import singleton_ScrubDb
from chromeDriver import singleton_chrome
import time
from config.myconfig import singleton as singleton_cfg


class WPSpider(object):
    # BASE_URL = 'https://bet.hkjc.com/default.aspx?url=/racing/pages/odds_wp.aspx&lang=ch&dv=local'
    # BASE_URL = 'https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=en&date=2019-01-16&venue=hv&raceno='

    def __init__(self):
        strDate = singleton_cfg.getRaceDate()
        self.BASE_URL = 'https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=en&date=' + strDate[:len(strDate)-4]\
                   + '-' + strDate[len(strDate)-4 : len(strDate)-2] + '-' + strDate[len(strDate)-2:] + '&venue=hv&raceno='

    def getRaceStartTime(self, race_date, race_time):
        race_date_text = str(race_date)
        if len(race_date_text) > 4:
            race_start_year = int(race_date_text[:len(race_date_text) - 4])
            race_start_month = int(race_date_text[len(race_date_text) - 4:len(race_date_text) - 2])
            race_start_day = int(race_date_text[len(race_date_text) - 2:])
        else:
            race_start_year = 0
            race_start_month = 0
            race_start_day = 0

        array_race_time = race_time.split(':')
        if len(array_race_time) == 2:
            race_start_hour = int(array_race_time[0])
            race_start_min = int(array_race_time[1])
        else:
            race_start_hour = 0
            race_start_min = 0
        return race_start_year, race_start_month, race_start_day, race_start_hour, race_start_min

    def start_requests(self, race_no):
        url = self.BASE_URL + str(race_no)
        print('request=>', url)
        try:
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            raceInfo = self.__parseRaceInfo()
            wpTable = self.__parseWPTable()
            if len(wpTable) > 0:
                self.updateWP(raceInfo, wpTable)
        except Exception as error:
            common.log('parse page error:' + str(error))

    def __parseRaceInfo(self):
        print('__parseRaceInfo')
        infoDict = {}
        infoDict['race_no'] = 0
        infoDict['race_date'] = 0
        infoDict['race_time'] = '00:00'
        infoDict['cls'] = 0
        infoDict['course'] = ''
        infoDict['distance'] = 0
        infoDict['going'] = ''
        tables = singleton_chrome.driver.find_elements_by_xpath('//table')
        if len(tables) > 8:
            tds = tables[8].find_elements_by_xpath('./tbody/tr/td')
            if len(tds) > 2:
                infoDict['race_no'] = int(tds[0].text.replace('Race', ''))
                raceInfo_text = tds[2].text
                array_raceInfo = raceInfo_text.split(',')
                if len(array_raceInfo) >= 7:
                    race_date_text = array_raceInfo[1].split('/')
                    if len(race_date_text) == 3:
                        infoDict['race_date'] = int(race_date_text[2].strip() + common.toDoubleDigitStr(race_date_text[1].strip()) + common.toDoubleDigitStr(race_date_text[0].strip()))

                    infoDict['race_time'] = array_raceInfo[2].strip()
                    infoDict['cls'] = array_raceInfo[3].replace('Class', '').replace(' ', '').strip()

                    if len(array_raceInfo) == 8:
                        array_course = array_raceInfo[5].split('"')
                        if len(array_course) > 1:
                            infoDict['course'] = array_course[1]
                        else:
                            infoDict['course'] = array_raceInfo[5]

                        infoDict['distance'] = int(array_raceInfo[6].replace('m', ''))
                        infoDict['going'] = array_raceInfo[7].replace(' ', '').upper()
                        if infoDict['going'] == '':
                            infoDict['going'] = 'GOOD'
                    else:
                        array_course = array_raceInfo[4].split('"')
                        if len(array_course) > 1:
                            infoDict['course'] = array_course[1].strip()
                        else:
                            infoDict['course'] = array_raceInfo[4].strip()

                        infoDict['distance'] = int(array_raceInfo[5].replace('m', ''))
                        infoDict['going'] = array_raceInfo[6].replace(' ', '').strip().upper()
                        if infoDict['going'] == '':
                            infoDict['going'] = 'GOOD'
        return infoDict

    def __parseWPTable(self):
        print('__parseWPTable')
        wpTable = {}    # horse_no & {key=>horse_name, draw, wt, jockey, trainer}
        divs = singleton_chrome.driver.find_elements_by_xpath('//div[@id="detailWPTable"]')
        if len(divs) > 0:
            tables = divs[0].find_elements_by_xpath('.//table')
            if len(tables) > 0:
                trs = tables[0].find_elements_by_xpath('./tbody/tr')
                if len(trs) > 0:
                    n = 0
                    for tr in trs[1:]:
                        tds = tr.find_elements_by_xpath('./td')
                        if len(tds) > 0:
                            if tds[0].text == 'F':
                                continue
                            horse_no = int(tds[0].text)
                            if len(tds) == 10:
                                if horse_no not in wpTable.keys():
                                    info = {}
                                    info['exit_race'] = False
                                    info['horse_code'] = tds[1].find_element_by_xpath('.//img').get_attribute('title').strip()
                                    info['horse_name'] = tds[2].text
                                    info['draw'] = int(tds[3].text)
                                    info['wt'] = int(tds[4].text)
                                    info['jockey'] = tds[5].text.strip()
                                    info['trainer'] = tds[6].text.strip()
                                    info['win_odds'] = tds[7].text
                                    info['pla_odds'] = tds[8].text
                                    info['win_pla'] = tds[9].text
                                    wpTable[horse_no] = info
                                else:
                                    common.log('horse[No.' + str(horse_no) + '] has added, parse page error')
                            else:
                                common.log('horse[No.' + str(horse_no) + '] has exit race')
                                info = {}
                                info['exit_race'] = True
                                wpTable[horse_no] = info
                    else:
                        pass
        for key, value in wpTable.items():
            print('parse page success=>', key, value)
        return wpTable

    # 若有马退赛，更新count
    def procExitHorse(self, raceInfo, exit_horse_no):
        common.log('procExitHorse:' + str(exit_horse_no))
        tableName = singleton_cfg.getUpdateResultsTable()
        # 删除退赛的马
        sql_delete = 'delete from {} where race_date=%s and race_no=%s and horse_no=%s'.format(tableName)
        singleton_ResultsDb.cursor.execute(sql_delete, (raceInfo['race_date'], raceInfo['race_no'], exit_horse_no))
        singleton_ResultsDb.connect.commit()
        # 计算现在的count
        singleton_ResultsDb.cursor.execute('select * from {} where race_date=%s and race_no=%s'.format(tableName), (raceInfo['race_date'], raceInfo['race_no']))
        allRows = singleton_ResultsDb.cursor.fetchall()
        singleton_ResultsDb.connect.commit()
        newCount = len(allRows)
        common.log('new count:' + str(newCount))
        # 修改本场比赛所有马匹的count值
        sql_update = 'update {} set count=%s where race_date=%s and race_no=%s'.format(tableName)
        singleton_ResultsDb.cursor.execute(sql_update, (newCount, raceInfo['race_date'], raceInfo['race_no']))
        singleton_ResultsDb.connect.commit()

    def updateWP(self, raceInfo, wpTable):
        print('\nupdateWP raceInfo:', raceInfo)
        if raceInfo['race_date'] == 0 or raceInfo['race_no'] == 0:
            return
        # 更新result库中相关表字段
        tableName_results = singleton_cfg.getUpdateResultsTable()
        if singleton_ResultsDb.table_exists(tableName_results):
            for horse_no, info in wpTable.items():
                if info['exit_race']:
                    # 若发现有退赛的马匹，删除
                    common.log('Results: 退赛 race_no[' + str(raceInfo['race_no']) + '] horse_no[' + str(horse_no) + ']')
                    self.procExitHorse(raceInfo, horse_no)
                else:
                    sql_select = 'select horse_code from {} where race_date=%s and race_no=%s and horse_no=%s'.format(tableName_results)
                    singleton_ResultsDb.cursor.execute(sql_select, (raceInfo['race_date'], raceInfo['race_no'], horse_no))
                    row = singleton_ResultsDb.cursor.fetchone()
                    singleton_ResultsDb.connect.commit()
                    if row:
                        if row['horse_code'] != info['horse_code']:
                            common.log("Results: 马匹更换 horse_no[" + str(horse_no) + '] race_no[' + str(raceInfo['race_no']) + ']:'
                                       + row['horse_code'] + '=>' + info['horse_code'])
                        else:
                            sql_update = '''update {} set draw=%s,win_odds=%s,pla_odds=%s,going=%s,actual_wt=%s 
                            where race_date=%s and race_no=%s and horse_no=%s and horse_code=%s'''.format(tableName_results)
                            singleton_ResultsDb.cursor.execute(sql_update, (info['draw'], info['win_odds'], info['pla_odds'], raceInfo['going'], info['wt'],
                                                                            raceInfo['race_date'], raceInfo['race_no'], horse_no, info['horse_code']))
                            singleton_ResultsDb.connect.commit()
                    else:
                        # 有新加入的马匹，添加
                        common.log('Results: 新马匹加入 race_no[' + str(raceInfo['race_no']) + '] horse_no[' + str(horse_no) + ']')
        else:
            common.log('table[' + tableName_results + '] not exist')

        # 更新scrub库中相关表字段
        common.log('\nscrub 库中i_odds表')
        tableName_scrub = singleton_cfg.getUpdateScrubTable()
        if singleton_ScrubDb.table_exists(tableName_scrub):
            for horse_no, info in wpTable.items():
                if info['exit_race']:
                    # 若发现有退赛的马匹，无视，不更新表中数据
                    pass
                else:
                    sql_select = 'select horse_code,jockey,trainer from {} where race_date=%s and race_no=%s and horse_no=%s'.format(tableName_scrub)
                    singleton_ScrubDb.cursor.execute(sql_select, (str(raceInfo['race_date']), raceInfo['race_no'], horse_no))
                    row = singleton_ScrubDb.cursor.fetchone()
                    singleton_ScrubDb.connect.commit()
                    if row:
                        if row['horse_code'] != info['horse_code']:
                            common.log("Scrub: 马匹更换 horse_no[" + str(horse_no) + '] race_no[' + str(raceInfo['race_no']) + ']:'
                                       + row['horse_code'] + '=>' + info['horse_code'])
                        if row['jockey'] != info['jockey']:
                            common.log("Scrub: 骑师更换 horse_no[" + str(horse_no) + '] race_no[' + str(raceInfo['race_no']) + ']:'
                                       + row['horse_code'] + '=>' + info['horse_code'])
                        if row['trainer'] != info['trainer']:
                            common.log("Scrub: 练马师更换 horse_no[" + str(horse_no) + '] race_no[' + str(raceInfo['race_no']) + ']:'
                                       + row['horse_code'] + '=>' + info['horse_code'])
                        # 无论马匹是否更换，均记录相关字段即时信息
                        sql_update = '''update {} set draw=%s,win_odds=%s,pla_odds=%s,going=%s,actual_wt=%s,jockey=%s,trainer=%s
                        where race_date=%s and race_no=%s and horse_no=%s and horse_code=%s'''.format(tableName_scrub)
                        singleton_ScrubDb.cursor.execute(sql_update, (info['draw'], info['win_odds'], info['pla_odds'], raceInfo['going'], info['wt'], info['jockey'], info['trainer'],
                                                                        str(raceInfo['race_date']), raceInfo['race_no'], horse_no, info['horse_code']))
                        singleton_ScrubDb.connect.commit()
                    else:
                        # 有新加入的马匹，添加
                        common.log('Scrub: 新马匹加入 race_no[' + str(raceInfo['race_no']) + '] horse_no[' + str(horse_no) + ']')
                        sql_insert = '''insert into {}(race_date,race_no,horse_no,horse_code,draw,win_odds,pla_odds,going,actual_wt,jockey,trainer) 
                        value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(tableName_scrub)
                        singleton_ScrubDb.cursor.execute(sql_insert, (raceInfo['race_date'], raceInfo['race_no'], horse_no, info['horse_code'],
                                                                      info['draw'], info['win_odds'], info['pla_odds'], raceInfo['going'], info['wt'], info['jockey'], info['trainer']))
                        singleton_ScrubDb.connect.commit()
        else:
            common.log('table[' + tableName_scrub + '] not exist')
        pass

    def __del__(self):
        print('===== spider over ====')

