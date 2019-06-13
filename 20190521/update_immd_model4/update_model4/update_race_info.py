from db.db import singleton_ResultsDb
from update_model4 import update_data_horse
from update_model4 import update_data_trainer
from update_model4 import update_data_jockey
from update_model4 import update_data_going
from update_model4 import update_data_draw
from update_model4 import update_data_actual_wt
from update_model4 import update_data_win_odds
from common import common


def __getCurRow(lastest_rows, race_No, horse_No):
    if (race_No in lastest_rows.keys()) and (horse_No in lastest_rows[race_No].keys()):
        return lastest_rows[race_No][horse_No]
    return None


def __updateDb(update_table, title, race_No, horse_No, cur_value):
    sql_update = 'update {} set '.format(update_table) + title + '=%s where race_no=%s and horse_no=%s'
    singleton_ResultsDb.cursor.execute(sql_update, (cur_value, race_No, horse_No))
    singleton_ResultsDb.connect.commit()


def __deleteFromDb(update_table, race_date, race_No, horse_No):
    sql_update = 'delete from {} where race_date=%s and race_no=%s and horse_no=%s'.format(update_table)
    singleton_ResultsDb.cursor.execute(sql_update, (race_date, race_No, horse_No))
    singleton_ResultsDb.connect.commit()


def __updateRelativeData(race_results_rows, race_card_history_rows, display_sectional_time_rows, immd_rows,
                         today_race_start_time, update_table, race_No, horse_No, update_keys, cur_row, prev_row):
    if 'horse_code' in update_keys:
        update_data_horse.updateData(race_results_rows, race_card_history_rows, display_sectional_time_rows, cur_row,
                                     prev_row, update_table, race_No, horse_No)
    if 'trainer' in update_keys:
        update_data_trainer.updateData(race_results_rows, cur_row, update_table, race_No, horse_No)
    if 'jockey' in update_keys:
        update_data_jockey.updateData(race_results_rows, cur_row, update_table, race_No, horse_No)
    if 'going' in update_keys:
        update_data_going.updateData(race_results_rows, display_sectional_time_rows, cur_row, prev_row, update_table, race_No, horse_No)
    if 'draw' in update_keys:
        update_data_draw.updateData(race_results_rows, cur_row, update_table, race_No, horse_No)
    if 'actual_wt' in update_keys:
        update_data_actual_wt.updateData(race_results_rows, race_card_history_rows, cur_row, update_table, race_No, horse_No)
    if 'win_odds' in update_keys:
        update_data_win_odds.updateData(race_results_rows, immd_rows, today_race_start_time, cur_row, update_table, race_No, horse_No)
    if 'pla_odds' in update_keys:
        pass


def updateModel4(update_table, dict, immd_rows, lastest_rows, race_results_rows, race_card_history_rows,
                   display_sectional_time_rows, today_race_start_time):
    for race_No, rows in dict.items():
        for horse_No, prev_row in rows.items():
            print('\nrace_No[', race_No, '] horse_No[', horse_No, '] update model4')
            update_keys = []
            cur_row = __getCurRow(lastest_rows, race_No, horse_No)
            if cur_row != None:
                # print('cur_row:', cur_row)
                # exit_race
                cur_exit_race = cur_row['exit_race']
                cur_race_date = cur_row['race_date']
                if cur_exit_race == 1:
                    print('horse exit race:', race_No, ' horse_no=', horse_No)
                    __deleteFromDb(update_table, cur_race_date, race_No, horse_No)
                    continue
                # win_odds
                if 'SCR' not in cur_row['win_odds']:
                    prev_win_odds = prev_row['win_odds']
                    cur_win_odds = float(cur_row['win_odds'])
                    if cur_win_odds != prev_win_odds:
                        print('update win_odds:', race_No, ' horse_no=', horse_No, prev_win_odds, '=>', cur_win_odds)
                        __updateDb(update_table, 'win_odds', race_No, horse_No, cur_win_odds)
                        update_keys.append('win_odds')
                # pla_odds
                if 'SCR' not in cur_row['pla_odds']:
                    prev_pla_odds = prev_row['pla_odds']
                    cur_pla_odds = float(cur_row['pla_odds'])
                    if cur_pla_odds != prev_pla_odds:
                        print('update pla_odds:', race_No, ' horse_no=', horse_No, prev_pla_odds, '=>', cur_pla_odds)
                        __updateDb(update_table, 'pla_odds', race_No, horse_No, cur_pla_odds)
                        update_keys.append('pla_odds')
                # horse_code
                prev_horse_code = prev_row['horse_code']
                cur_horse_code = cur_row['horse_code']
                if cur_horse_code != prev_horse_code:
                    common.log('update horse_code:' + str(race_No) + ' horse_no=' + str(horse_No) + ' prev/old:' + prev_horse_code + '=>' + cur_horse_code)
                    __updateDb(update_table, 'horse_code', race_No, horse_No, cur_horse_code)
                    update_keys.append('horse_code')
                # trainer_code
                prev_trainer = prev_row['trainer_code']
                cur_trainer = cur_row['trainer']
                if prev_trainer != cur_trainer:
                    common.log('update trainer:' + str(race_No) + ' horse_no=' + str(horse_No) + ' prev/old:' + prev_trainer + '=>' + cur_trainer)
                    __updateDb(update_table, 'trainer_code', race_No, horse_No, cur_trainer)
                    update_keys.append('trainer')
                # jockey_code
                prev_jockey = prev_row['jockey_code']
                cur_jockey = cur_row['jockey']
                if prev_jockey != cur_jockey:
                    common.log('update jockey:' + str(race_No) + ' horse_no=' + str(horse_No) + ' prev/old:' + prev_jockey + '=>' + cur_jockey)
                    __updateDb(update_table, 'jockey_code', race_No, horse_No, cur_jockey)
                    update_keys.append('jockey')
                # going
                prev_going = prev_row['going']
                cur_going = cur_row['going']
                if prev_going != cur_going:
                    common.log('update going:' + str(race_No) + ' horse_no=' + str(horse_No) + ' prev/old:' + prev_going + '=>' + cur_going)
                    __updateDb(update_table, 'going', race_No, horse_No, cur_going)
                    update_keys.append('going')
                # draw_label
                prev_draw = prev_row['draw_label']
                cur_draw= cur_row['draw']
                if prev_draw != cur_draw:
                    common.log('update draw:' + str(race_No) + ' horse_no=' + str(horse_No) + ' prev/old:' + prev_draw + '=>' + cur_draw)
                    __updateDb(update_table, 'draw_label', race_No, horse_No, cur_draw)
                    update_keys.append('draw')
                # actual_wt
                prev_actual_wt = prev_row['actual_wt']
                cur_actual_wt = cur_row['wt']
                if prev_actual_wt != cur_actual_wt:
                    common.log('update actual_wt:' + str(race_No) + ' horse_no=' + str(horse_No) + ' prev/old:' + prev_actual_wt + '=>' + cur_actual_wt)
                    __updateDb(update_table, 'actual_wt', race_No, horse_No, cur_actual_wt)
                    update_keys.append('actual_wt')
                __updateRelativeData(race_results_rows, race_card_history_rows, display_sectional_time_rows,
                                     immd_rows, today_race_start_time, update_table, race_No, horse_No, update_keys,
                                     cur_row, prev_row)
    singleton_ResultsDb.connect.commit()

