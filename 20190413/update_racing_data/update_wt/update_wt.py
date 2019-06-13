from db.db import singleton_ResultsDb
from config.myconfig import singleton_cfg
from common import common


def __getLastestWt(lastest_dict):
    wt_dict = {}  # race_no & {horse_no & wt}
    for race_no, dict in lastest_dict.items():
        if race_no not in wt_dict.keys():
            wt_dict[race_no] = {}
        for horse_no, row in dict.items():
            if row['exit_race'] == 1:   # 退赛的wt不更新
                continue
            wt_dict[race_no][horse_no] = row['wt']
    return wt_dict


# lastest_dict: race_no & {horse_no & row}
def updateWt(today_table_dict, lastest_dict):
    wt_dict = __getLastestWt(lastest_dict)  # race_no & {horse_no & wt}
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if update_table in today_table_dict.keys():
            today_table = today_table_dict[update_table]
            for race_no, dict in today_table.items():
                for horse_no, row in dict.items():
                    if (race_no in wt_dict.keys()) and (horse_no in wt_dict[race_no].keys()):
                        new_wt = wt_dict[race_no][horse_no]
                        old_wt = row['actual_wt']
                        if old_wt != new_wt:
                            print('update wt: race_no=', race_no, ' horse_no=', horse_no)
                            singleton_ResultsDb.cursor.execute('update {} set actual_wt=%s where race_no=%s and horse_no=%s'.format(update_table), (new_wt, race_no, horse_no))
                            singleton_ResultsDb.connect.commit()
                    else:
                        common.log("[wt]don't find horse[" + str(horse_no) + '] in race[' + str(race_no) + ']')
