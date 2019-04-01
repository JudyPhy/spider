###     获取比赛前的current_rating     ###
### current_rating数据来源表: a_future_horse_info_YMD ###
from db.database import singleton_Scrub_DB
from common import common
import datetime

HISTORY_RACE_CARD_TABLE = 't_race_card_{0}'


# 根据比赛前爬取的马匹数据，获取对应时间的current rating
def __getCurrentRatingBeforeDict():
    results_dict = {}   # race_date & {horse_code & current_rating}
    repeat_race_date = []
    tableList = common.getFutureHorseTableList()
    for table in tableList:
        if singleton_Scrub_DB.table_exists(table):
            singleton_Scrub_DB.cursor.execute('select race_date,code,current_rating from {}'.format(table))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                race_date = int(row['race_date'])
                if race_date not in results_dict.keys():
                    results_dict[race_date] = {}
                horse_code = row['code'].strip()
                if horse_code not in results_dict[race_date].keys():
                    results_dict[race_date][horse_code] = row['current_rating']
                else:
                    if race_date not in repeat_race_date:
                        repeat_race_date.append(race_date)
        else:
            print('current_rating: Table[' + table + '] not exist')
    if len(repeat_race_date) > 0:
        msg = ''
        for date in repeat_race_date:
            msg += str(date) + ','
        print('current_rating: repeat_race_date=>' + msg)
    return results_dict


def getRtg():
    rtg_dict = {}  # race_date(int) & {horse_code & rtg}
    now = datetime.datetime.now()
    for year in range(2014, now.year + 1):
        tableName = HISTORY_RACE_CARD_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute('select race_date,horse_code,rtg from {}'.format(tableName))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                race_date = int(row['race_date'])
                if race_date not in rtg_dict.keys():
                    rtg_dict[race_date] = {}
                horse_code = row['horse_code']
                if horse_code not in rtg_dict[race_date].keys():
                    if '-' in row['rtg']:
                        rtg_dict[race_date][horse_code] = 0
                    else:
                        rtg_dict[race_date][horse_code] = int(row['rtg'])
                else:
                    print(race_date, horse_code, 'rtg repeat')
        else:
            print('current_rating: Table[' + tableName + '] not exist')

    count = 0
    for race_date, dict in rtg_dict.items():
        count += len(dict)
    print('rtg len=', count)
    return rtg_dict


def getCurrentRatingBeforeRace():
    before_dict = __getCurrentRatingBeforeDict()  # race_date & {horse_code & current_rating}
    count = 0
    for race_date, dict in before_dict.items():
        count += len(dict)
    print('current_rating len=', count)
    return before_dict



