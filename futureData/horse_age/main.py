###  根据爬取的当天马匹信息数据得到马匹年龄  ###
from db.database import singleton_Scrub_DB
from common import common
from config.myconfig import singleton_cfg

TODAY_HORSE_FROM_TABLE = singleton_cfg.getTodayHorseInfoTable()


# 因当日比赛马匹不会是退役马匹，所以直接从当日比赛马匹信息表中获取年龄
def getTodayHorseAgeDict():
    age_dict = {}   # horse_code & age
    if singleton_Scrub_DB.table_exists(TODAY_HORSE_FROM_TABLE):
        singleton_Scrub_DB.cursor.execute('select code,age from {}'.format(TODAY_HORSE_FROM_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            horse_code = row['code']
            if horse_code not in age_dict.keys():
                age_dict[horse_code] = row['age']
            else:
                common.log('horse_age: horse[' + horse_code + '] repeat in today horse info table')
    else:
        common.log('horse_age: table[' + TODAY_HORSE_FROM_TABLE + '] not exist')
    return age_dict

