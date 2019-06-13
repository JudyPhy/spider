from db.db import singleton_ResultsDb
from common import common
from config.myconfig import singleton_cfg


def __getLastestExitRace(lastest_dict):
    exitRace_dict = {}  # race_no & {horse_no & exit_race}
    for race_no, dict in lastest_dict.items():
        if race_no not in exitRace_dict.keys():
            exitRace_dict[race_no] = {}
        for horse_no, row in dict.items():
            if row['exit_race'] == 1:
                exitRace_dict[race_no][horse_no] = True
            else:
                exitRace_dict[race_no][horse_no] = False
    return exitRace_dict


def __updateCount(update_table, race_date, race_no):
    if 'model2' not in update_table:
        return
    singleton_ResultsDb.cursor.execute('select * from {} where race_date=%s and race_no=%s'.format(update_table),
                                       (int(race_date), race_no))
    rows = singleton_ResultsDb.cursor.fetchall()
    new_count = len(rows)
    common.log('race_no[' + str(race_no) + '] new count=' + str(new_count))
    singleton_ResultsDb.cursor.execute('update {} set count=%s where race_date=%s and race_no=%s'.format(update_table),
                                       (new_count, int(race_date), race_no))
    singleton_ResultsDb.connect.commit()


def updateExitRace(today_table_dict, lastest_dict):
    race_date = singleton_cfg.getRaceDate()
    exitRace_dict = __getLastestExitRace(lastest_dict)
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if update_table in today_table_dict.keys():
            today_table = today_table_dict[update_table]
            for race_no, dict in exitRace_dict.items():
                for horse_no, exit in dict.items():
                    if (race_no in today_table.keys()) and (horse_no in today_table[race_no].keys()):
                        if exit:
                            # 退赛, 删除对应马匹
                            common.log('退赛: race_no=' + str(race_no) + ' horse_no=' + str(horse_no))
                            singleton_ResultsDb.cursor.execute('delete from {} where race_date=%s and race_no=%s and horse_no=%s'.format(update_table),
                                                               (int(race_date), race_no, horse_no))
                            singleton_ResultsDb.connect.commit()
                            __updateCount(update_table, race_date, race_no)
                        else:
                            # 保持不变
                            pass
                    else:
                        if exit:
                            # 退赛马匹，并已经在today表中删除
                            pass
                        else:
                            common.log('退赛后又重新参赛: race_no=' + str(race_no) + ' horse_no=' + str(horse_no))

