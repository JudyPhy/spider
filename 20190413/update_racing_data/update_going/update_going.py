from db.db import singleton_ResultsDb
from config.myconfig import singleton_cfg
from common import common


def __getLastestGoing(lastest_dict):
    going_dict = {}  # race_no & {horse_no & going}
    for race_no, dict in lastest_dict.items():
        if race_no not in going_dict.keys():
            going_dict[race_no] = {}
        for horse_no, row in dict.items():
            if row['exit_race'] == 1:   # 退赛的going不更新
                continue
            going_dict[race_no][horse_no] = row['going']
    return going_dict


# lastest_dict: race_no & {horse_no & row}
def updateGoing(today_table_dict, lastest_dict):
    going_dict = __getLastestGoing(lastest_dict)  # race_no & {horse_no & going}
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if update_table in today_table_dict.keys():
            today_table = today_table_dict[update_table]
            for race_no, dict in today_table.items():
                for horse_no, row in dict.items():
                    if (race_no in going_dict.keys()) and (horse_no in going_dict[race_no].keys()):
                        new_going = going_dict[race_no][horse_no]
                        old_going = row['going']
                        if old_going != new_going:
                            common.log('update going: race_no=' + str(race_no) + ' horse_no=' + str(horse_no) + ' old=' + old_going + ' new=' + new_going)
                            singleton_ResultsDb.cursor.execute('update {} set going=%s where race_no=%s and horse_no=%s'.format(update_table),
                                                               (new_going, race_no, horse_no))
                            singleton_ResultsDb.connect.commit()
                    else:
                        common.log("[going]don't find horse[" + str(horse_no) + '] in race[' + str(race_no) + ']')
