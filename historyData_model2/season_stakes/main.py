###     ��ȡ����ǰ��season_stakes    ###
### current_rating������Դ��: a_future_horse_info_YMD ###
from db.database import singleton_Scrub_DB
from common import common


# ���ݱ���ǰ��ȡ����ƥ���ݣ���ȡ��Ӧʱ���season_stakes
def __getSeasonStakesBeforeDict():
    results_dict = {}   # race_date & {horse_code & season_stakes}
    repeat_race_date = []
    tableList_future = common.getFutureHorseTableList()
    for table in tableList_future:
        if singleton_Scrub_DB.table_exists(table):
            singleton_Scrub_DB.cursor.execute('select race_date,code,season_stakes from {}'.format(table))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                race_date = int(row['race_date'])
                if race_date not in results_dict.keys():
                    results_dict[race_date] = {}
                horse_code = row['code']
                if horse_code not in results_dict[race_date].keys():
                    results_dict[race_date][horse_code] = row['season_stakes']
                else:
                    if race_date not in repeat_race_date:
                        repeat_race_date.append(race_date)
        else:
            print('season_stakes: Table[' + table + '] not exist')
    if len(repeat_race_date) > 0:
        msg = ''
        for date in repeat_race_date:
            msg += str(date) + ','
        print('season_stakes: repeat_race_date=>' + msg)
    return results_dict


def getSeasonStakesBeforeRace():
    before_dict = __getSeasonStakesBeforeDict()  # race_date & {horse_code & season_stakes}
    return before_dict



