from config.myconfig import singleton_cfg
from db.db import singleton_ScrubDb

RACE_CARD_TABLEA = 't_race_card_future_{0}'


def getTodayRaceCardTable():
    today_dict = {}  # race_no & {horse_no & row}
    race_date = singleton_cfg.getRaceDate()
    race_card_table = RACE_CARD_TABLEA.replace('{0}', race_date[: len(race_date) - 4])
    if singleton_ScrubDb.table_exists(race_card_table):
        singleton_ScrubDb.cursor.execute('select * from {}'.format(race_card_table))
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_no = row['race_no']
            horse_no = row['horse_no']
            if race_no not in today_dict.keys():
                today_dict[race_no] = {}
            today_dict[race_no][horse_no] = row
    else:
        print('today table[', race_card_table, '] not exist')
    return today_dict

