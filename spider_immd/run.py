from wpSpider import WPSpider
import datetime
from db.db import singleton_ScrubDb
from config.myconfig import singleton as singleton_cfg
from common import common


def __parseRaceStartTime(race_date, race_time):
    race_date_text = str(race_date.strip())
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


# 计算当前和比赛开始之间的时间差
def __getDeltaSeconds(race_start_time):
    array_race_time = race_start_time.split(':')
    if len(array_race_time) == 2:
        race_start_year, race_start_month, race_start_day, race_start_hour, race_start_min = parseRaceStartTime(singleton_cfg.getRaceDate(), race_start_time)
        d_end = datetime.datetime(race_start_year, race_start_month, race_start_day, race_start_hour, race_start_min, 0)
        d_start = datetime.datetime.now()
        delta_time = d_end - d_start
        return delta_time.total_seconds()
    return None


def getRaceStartTime():
    race_start_time_dict = {}   # race_no & start_time
    tableName = 't_race_card_' + singleton_cfg.getRaceDate().strip()
    if singleton_ScrubDb.table_exists(tableName):
        for race_no in range(1, 12):
            singleton_ScrubDb.cursor.execute('select race_time from {} where race_date=%s and race_no=%s'.format(tableName),
                                             (singleton_cfg.getRaceDate().strip(), race_no))
            row = singleton_ScrubDb.cursor.fetchone()
            if row:
                race_start_time_dict[race_no] = row['race_time']
    else:
        common.log('table[' + tableName + '] not exist')
    return race_start_time_dict


def request():
    race_start_time_dict = getRaceStartTime()   # race_no & start_time
    sorted_raceNo = sorted(race_start_time_dict.keys())
    while (True):
        # 获取即将开始的比赛场次
        racingNo = 0
        for race_no in sorted_raceNo:
            start_time = race_start_time_dict[race_no]
            deltaSec = __getDeltaSeconds(start_time)
            if deltaSec > 0:
                racingNo = race_no
                break
        common.log('即将开始的比赛场次为：' + str(racingNo))
        if racingNo == 0:
            last_raceNo = sorted_raceNo[len(sorted_raceNo) - 1]
            last_deltaSec = __getDeltaSeconds(race_start_time_dict[last_raceNo])
            print('比赛已经结束时间：', last_deltaSec)
            if last_deltaSec < 0 and last_deltaSec > -1*60*60:
                common.log('所有比赛结束，继续顺序爬取所有比赛1小时')
                for race_no in sorted_raceNo:
                    WPSpider().start_requests(race_no)
                continue
            else:
                break

        # 在racingNo开场前10分钟，只爬取本场比赛，其余时间段全部爬取
        racing_deltaSec = __getDeltaSeconds(race_start_time_dict[racingNo])
        min = int(racing_deltaSec/60)
        sec = racing_deltaSec - min*60
        common.log('距离比赛开场时间:' + str(min) + ':' + str(sec))
        if racing_deltaSec < 5*60:
            common.log('单独爬取第' + str(racingNo) + '场比赛')
            WPSpider().start_requests(racingNo)
        else:
            common.log('顺序爬取所有比赛')
            for race_no in sorted_raceNo:
                WPSpider().start_requests(race_no)
    print('all race over')


request()



