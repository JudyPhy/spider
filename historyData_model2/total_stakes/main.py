###     获取比赛前的total_stakes    ###
### current_rating数据来源表: a_future_horse_info_YMD ###
from db.database import singleton_Scrub_DB
from config.myconfig import singleton_cfg
from common import common

# BEFORE_TABLE_LIST = singleton_cfg.getCurrentRatingBeforeTableList()


# 根据比赛前爬取的马匹数据，获取对应时间的total_stakes
def __getTotalStakesBeforeDict():
    results_dict = {}   # race_date & {horse_code & total_stakes }
    repeat_race_date = []
    tableList_future = common.getFutureHorseTableList()
    for table in tableList_future:
        array_race_date = table.split('_')
        race_date = int(array_race_date[len(array_race_date) - 1])
        if race_date not in results_dict.keys():
            results_dict[race_date] = {}
        if singleton_Scrub_DB.table_exists(table):
            singleton_Scrub_DB.cursor.execute('select code,total_stakes from {}'.format(table))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                horse_code = row['code']
                if horse_code not in results_dict[race_date].keys():
                    results_dict[race_date][horse_code] = row['total_stakes']
                else:
                    if race_date not in repeat_race_date:
                        repeat_race_date.append(race_date)
        else:
            common.log('total_stakes: Table[' + table + '] not exist')
    if len(repeat_race_date) > 0:
        msg = ''
        for date in repeat_race_date:
            msg += str(date) + ','
        common.log('total_stakes: repeat_race_date=>' + msg)
    return results_dict


def getTotalStakesBeforeRace():
    before_dict = __getTotalStakesBeforeDict()  # race_date & {horse_code & total_stakes}
    return before_dict



