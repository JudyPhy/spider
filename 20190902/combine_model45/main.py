# coding=gbk
from db import request_db_data
from db import exportToDb


def __getModel4Row(model4_rows, race_date_No, horse_No):
    if (race_date_No in model4_rows.keys()) and (horse_No in model4_rows[race_date_No].keys()):
        return model4_rows[race_date_No][horse_No]
    else:
        return None


def __getOddOldRows(odds_sectional_rows, odds_immd_sectional_rows):
    odds_old_dict = {}  # race_date_No & {horse_No & odd_old}
    # 先从苹果网提取
    for race_date_No, dict in odds_sectional_rows.items():
        if race_date_No not in odds_old_dict.keys():
            odds_old_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            odds_old_dict[race_date_No][horse_No] = row['odds3']

    # 再用immd表中数据覆盖
    for race_date_No, dict in odds_immd_sectional_rows.items():
        if race_date_No not in odds_old_dict.keys():
            odds_old_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            odds_old_dict[race_date_No][horse_No] = row['before10_odds']
    return odds_old_dict


def __getOddOld(odds_old_rows, race_date_No, horse_No):
    if (race_date_No in odds_old_rows.keys()) and (horse_No in odds_old_rows[race_date_No].keys()):
        if odds_old_rows[race_date_No][horse_No] != '':
            return float(odds_old_rows[race_date_No][horse_No])
    return 0


def main():
    model4_rows = request_db_data.RequestModel4Rows()  # race_date_No & {horse_No & row}
    model5_rows = request_db_data.RequestModel5Rows()   # race_date_No & {horse_No & row}
    odds_sectional_rows = request_db_data.RequestSectionalOddsRows()    # race_date_No & {horse_No & row}
    odds_immd_sectional_rows = request_db_data.RequestImmdSectionalOdds()  # race_date_No & {horse_No & row}
    odds_old_rows = __getOddOldRows(odds_sectional_rows, odds_immd_sectional_rows) # race_date_No & {horse_No & odd_old}
    all_list = []
    for race_date_No, row_dict in model5_rows.items():
        # print(race_date_No, row_dict)
        for horse_No, model5_row in row_dict.items():
            model4_row = __getModel4Row(model4_rows, race_date_No, horse_No)
            if model4_row:
                odd_old = __getOddOld(odds_old_rows, race_date_No, horse_No)
                cur_line = [model5_row['race_id'], model5_row['horse_no'], model5_row['pla_odds'],
                            model5_row['win_odds'], model5_row['plc'], model5_row['current_rating'],
                            odd_old, model5_row['odd_wave'], model5_row['dct_trend'],
                            model5_row['rating_trend'], model5_row['declar_horse_wt'], model5_row['actual_wt'],
                            model5_row['rest'], model5_row['horse_record_total'],
                            model5_row['horse_dst_record_total'], model5_row['horse_cls_record_total'],
                            model5_row['trainer_record_total'], model5_row['jockey_record_total'],
                            model5_row['jockey_recent_total'], model5_row['draw_record_total'],
                            model5_row['horse_best_speed'], model5_row['same_trainer_count'],
                            model5_row['horse_recent_total'], model5_row['horse_going_record_total'],
                            model5_row['jockey_fav_record_total'], model5_row['horse_gear_record_total'],
                            model5_row['horse_track_record_total'], model5_row['trainer_recent_total'],
                            model5_row['horse_fav_record_total'], model5_row['horse_track_fav_record_total'],
                            model5_row['trainer_fav_record_total'], model5_row['track_record_total'],
                            model5_row['horse_dst_record_before4'], model5_row['horse_cls_record_before4'],
                            model5_row['trainer_record_before4'], model5_row['jockey_record_before4'],
                            model5_row['jockey_recent_before4'], model5_row['draw_record_before4'],
                            model5_row['horse_recent_before4'], model5_row['horse_going_record_before4'],
                            model5_row['jockey_fav_record_before3'], model5_row['horse_gear_record_before4'],
                            model5_row['horse_track_record_before4'], model5_row['trainer_recent_before4'],
                            model5_row['horse_fav_record_before3'], model5_row['horse_track_fav_record_before3'],
                            model5_row['trainer_fav_record_before3'], model5_row['track_fav_record_before3'],
                            model5_row['horse_best_recent_speed'], model5_row['race_date'], model5_row['race_no'],
                            model5_row['horse_code'], model5_row['trainer'], model5_row['jockey'],
                            model5_row['site'], model5_row['going'], model5_row['course'], model5_row['dst'],
                            model5_row['cls'], model5_row['draw'], model5_row['gear'], model5_row['lbw'],
                            model5_row['finish_time'], model5_row['over_wt'], model5_row['cls_standard_speed'],
                            model5_row['pedigree_dst'], model5_row['pedigree_track'], model5_row['fav_match'],
                            model5_row['odd_diff'],
                            model4_row['jockey_trainer_record_total'], model4_row['horse_recent_record_total'],
                            model4_row['horse_go_record_total'], model4_row['jockey_hot'],
                            model4_row['horse_site_record_total'], model4_row['horse_course_record_total'],
                            model4_row['horse_draw_record_total'], model4_row['horse_jockey_record_total'],
                            model4_row['jockey_trainer_record_before4'], model4_row['horse_recent_record_before4'],
                            model4_row['horse_go_record_before4'], model4_row['horse_site_record_before4'],
                            model4_row['horse_course_record_before4'], model4_row['horse_draw_record_before4'],
                            model4_row['horse_jockey_record_before4'],
                            model4_row['horse_lowest_speed'], model4_row['horse_avr_speed'],
                            model4_row['horse_recent_best_speed'], model4_row['horse_recent_lowest_speed'],
                            model4_row['horse_recent_avr_speed'], model4_row['horse_site_best_speed'],
                            model4_row['horse_site_lowest_speed'], model4_row['horse_site_avr_speed'],
                            model4_row['horse_go_best_speed'], model4_row['horse_go_lowest_speed'],
                            model4_row['horse_go_avr_speed'], model4_row['horse_course_best_speed'],
                            model4_row['horse_course_lowest_speed'], model4_row['horse_course_avr_speed'],
                            model4_row['horse_dst_best_speed'], model4_row['horse_dst_lowest_speed'],
                            model4_row['horse_dst_avr_speed'], model4_row['horse_cls_best_speed'],
                            model4_row['horse_cls_lowest_speed'], model4_row['horse_cls_avr_speed'],
                            model4_row['horse_draw_best_speed'], model4_row['horse_draw_lowest_speed'],
                            model4_row['horse_draw_avr_speed'], model4_row['horse_gear_best_speed'],
                            model4_row['horse_gear_lowest_speed'], model4_row['horse_gear_avr_speed'],
                            model4_row['horse_jockey_best_speed'], model4_row['horse_jockey_lowest_speed'],
                            model4_row['horse_jockey_avr_speed'], model4_row['horse_last_dst_time_prev'],
                            model4_row['horse_last_dst_time_min'], model4_row['horse_last_dst_time_ave']]
                cur_line = (cur_line)
                all_list.append(cur_line)
            else:
                print('ERROR: model5 data loss', race_date_No, horse_No)
    exportToDb.exportToModel45Table(all_list)


main()
