from db.db import singleton_ResultsDb
from config.myconfig import singleton_cfg
from common import common
import datetime


def __getLastestOdds(lastest_dict):
    odds_dict = {}  # race_no & {horse_no & [win_odds, pla_odds]}
    for race_no, dict in lastest_dict.items():
        if race_no not in odds_dict.keys():
            odds_dict[race_no] = {}
        for horse_no, row in dict.items():
            if row['exit_race'] == 1:
                # 退赛的赔率不更新
                continue
            odds_dict[race_no][horse_no] = [float(row['win_odds']), float(row['pla_odds'])]
    return odds_dict


# lastest_dict: race_no & {horse_no & row}
def updateOdds(today_table_dict, lastest_dict):
    odds_dict = __getLastestOdds(lastest_dict)  # race_no & {horse_no & [win_odds, pla_odds]}
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if update_table in today_table_dict.keys():
            today_table = today_table_dict[update_table]
            for race_no, dict in today_table.items():
                for horse_no, row in dict.items():
                    if (race_no in odds_dict.keys()) and (horse_no in odds_dict[race_no].keys()):
                        odds = odds_dict[race_no][horse_no]
                        old_odds = [row['win_odds'], row['pla_odds']]
                        if (odds[0] != -1) and (odds[0] != old_odds[0]):
                            print('update win_odds:', race_no, ' horse_no=', horse_no)
                            singleton_ResultsDb.cursor.execute('update {} set win_odds=%s where race_no=%s and horse_no=%s'.format(update_table),
                                                               (odds[0], race_no, horse_no))
                            singleton_ResultsDb.connect.commit()
                        if (odds[1] != -1) and (odds[1] != old_odds[1]):
                            print('update pla_odds: race_no=', race_no, ' horse_no=', horse_no)
                            singleton_ResultsDb.cursor.execute('update {} set pla_odds=%s where race_no=%s and horse_no=%s'.format(update_table),
                                                               (odds[1], race_no, horse_no))
                            singleton_ResultsDb.connect.commit()
                    else:
                        common.log("[odds]don't find horse[" + str(horse_no) + '] in race[' + str(race_no) + ']')


