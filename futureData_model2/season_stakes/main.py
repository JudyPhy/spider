###     获取比赛前的season_stakes    ###
from db.database import singleton_Scrub_DB
from common import common
from config.myconfig import singleton_cfg

TODAY_HORSE_TABLE = singleton_cfg.getTodayHorseInfoTable()


def getTodaySeasonStakesBeforeRace():
    results_dict = {}  # horse_code & season_stakes
    if singleton_Scrub_DB.table_exists(TODAY_HORSE_TABLE):
        singleton_Scrub_DB.cursor.execute('select code,season_stakes from {}'.format(TODAY_HORSE_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            if row['code'] not in results_dict.keys():
                results_dict[row['code']] = row['season_stakes']
            else:
                common.log('horse[' + row['code'] + '] repeat in today horse info table')
    else:
        common.log('season_stakes: table[' + TODAY_HORSE_TABLE + '] not exist')
    return results_dict




