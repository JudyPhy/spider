###  根据比赛前爬取的马匹信息数据，获得current_rating ###
### current_rating数据来源表: a_future_horse_info_YMD ###
from db.database import singleton_Scrub_DB
from config.myconfig import singleton_cfg
from common import common

TODAY_HORSE_TABLE = singleton_cfg.getTodayHorseInfoTable()


def getTodayCurrentRatingBeforeRace():
    results_dict = {}  # horse_code & current_rating
    if singleton_Scrub_DB.table_exists(TODAY_HORSE_TABLE):
        singleton_Scrub_DB.cursor.execute('select code,current_rating from {}'.format(TODAY_HORSE_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            if row['code'] not in results_dict.keys():
                results_dict[row['code']] = row['current_rating']
            else:
                common.log('horse[' + row['code'] + '] repeat in today horse info table')
    else:
        common.log('current rating: table[' + TODAY_HORSE_TABLE + '] not exist')
    return results_dict


