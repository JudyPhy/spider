### 根据合并表的数据，制作新结构的数据表 ###
from db import request_db_data
from common import common
from dragon import source_datas
from dragon import export
import datetime


def isOddsLowest(win_odds, rows):
    for horse_code, row in rows.items():
        cur_plc = row['plc'].replace('DH', '')
        if cur_plc not in common.words:
            cur_odds = float(row['win_odds'])
            if cur_odds < win_odds:
                return False
    return True


def test(sort_history_raceCard_rows, sort_history_raceResults_rows, horse_pedigree_rows, display_sectional_time_rows, odds_sectional_rows):
    records = []
    for race_date_No, dict in sort_history_raceCard_rows.items():
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_date = int(race_date_No[: len(race_date_No) - 2])
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if (cur_date > 20160900) and (cur_plc not in common.words):
                    cur_distance = int(sort_history_raceResults_rows[race_date_No][horse_code]['distance'])
                    cur_site = sort_history_raceResults_rows[race_date_No][horse_code]['site'].replace(' ', '')
                    cur_course = sort_history_raceResults_rows[race_date_No][horse_code]['course'].strip()
                    if '"' in cur_course:
                        array_course = cur_course.split('"')
                        cur_course = array_course[1].strip()
                    cur_draw = int(sort_history_raceResults_rows[race_date_No][horse_code]['draw'])
                    cur_odds = float(sort_history_raceResults_rows[race_date_No][horse_code]['win_odds'])
                    cur_is_lowest_odds = isOddsLowest(cur_odds, sort_history_raceResults_rows[race_date_No])
                    if (cur_distance == 1200) and (cur_site == 'ShaTin') and (cur_course == 'A') and \
                            (cur_is_lowest_odds == True) and (int(cur_plc) < 4):
                        if race_date_No not in records:
                            records.append(race_date_No)
    print('\n\nrecords:', len(records))


def main():
    today = datetime.datetime.now()
    today_date = str(today.year) + common.toDoubleDigitStr(today.month) + common.toDoubleDigitStr(today.day)
    sort_history_raceCard_rows = request_db_data.RequestSortedHistoryRaceCardRows(today_date)  # race_date_No & {horse_code & row}
    sort_history_raceResults_rows = request_db_data.RequestSortedHistoryRaceResultsRows(today_date)  # race_date_No & {horse_code & row}
    horse_pedigree_rows = request_db_data.RequestHorsePedigreeRows()  # horse_code & row
    odds_sectional_rows = request_db_data.RequestSectionalOddsRows()  # race_date_No & {horse_No & row}
    course_standard_times_rows = request_db_data.RequestCourseStandardTimes()  # race_date_No & {horse_No & row}
    if len(sort_history_raceCard_rows) > 0:
        data_dict = source_datas.prepareDatas(sort_history_raceCard_rows, sort_history_raceResults_rows,
                                              horse_pedigree_rows, course_standard_times_rows, odds_sectional_rows)
        all_list = []
        print('start data=>')
        for race_date_No, dict in sort_history_raceCard_rows.items():
            for horse_code, row in dict.items():
                if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                    plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                    if plc not in common.words:
                        race_date = row['race_date']
                        race_no = row['race_No']
                        race_id = source_datas.getRaceId(race_date_No, horse_code, sort_history_raceResults_rows)
                        horse_no = row['horse_No']
                        pla_odds = 1
                        win_odds = source_datas.getValue(race_date_No, horse_code, data_dict['race_info']['win_odds_dict'], -1)
                        array_trainer = row['trainer'].split('(')
                        trainer = array_trainer[0].strip()
                        array_jockey = row['jockey'].split('(')
                        jockey = array_jockey[0].strip()
                        site = row['site'].replace(' ', '')
                        going = source_datas.getValue(race_date_No, horse_code, data_dict['race_info']['going_dict'], 'GOOD')
                        course = row['course'].strip()
                        if '"' in course:
                            array_course = course.split('"')
                            course = array_course[1].strip()
                        dst = int(row['distance'])
                        cls = row['cls'].strip()
                        draw = int(row['draw'])
                        gear = row['gear'].strip()

                        horse_records = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_record'])
                        horse_recent_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_recent_record'])
                        horse_fav_record = source_datas.getFavRecords(race_date_No, horse_code, data_dict['horse_fav_record'])
                        horse_site_course_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_site_course_record'])
                        horse_site_course_fav_record = source_datas.getFavRecords(race_date_No, horse_code, data_dict['horse_site_course_fav_record'])
                        horse_going_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_going_record'])
                        horse_dst_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_dst_record'])
                        horse_cls_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_cls_record'])
                        horse_gear_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_gear_record'])

                        best_time = row['best_time'].strip()
                        if best_time == '':
                            horse_best_speed = 0
                        else:
                            horse_best_speed = dst/common.GetTotalSeconds(best_time)
                        lbw = sort_history_raceResults_rows[race_date_No][horse_code]['lbw'].strip()
                        finish_time = common.GetTotalSeconds(sort_history_raceResults_rows[race_date_No][horse_code]['finish_time'])

                        trainer_record = source_datas.getRecords(race_date, trainer, data_dict['trainer_record'])
                        trainer_recent = source_datas.getRecords(race_date, trainer, data_dict['trainer_recent'])
                        trainer_fav_record = source_datas.getFavRecords(race_date, trainer, data_dict['trainer_fav_record'])

                        jockey_record = source_datas.getRecords(race_date, jockey, data_dict['jockey_record'])
                        jockey_recent = source_datas.getRecords(race_date, jockey, data_dict['jockey_recent'])
                        jockey_fav_record = source_datas.getFavRecords(race_date, jockey, data_dict['jockey_fav_record'])

                        draw_record = source_datas.getRecords(race_date, draw, data_dict['draw_record'])
                        cur_track = site + '_' + course.upper()
                        track_fav_record = source_datas.getValue(race_date, cur_track, data_dict['track_fav_record'], 0)
                        track_record = source_datas.getValue(race_date, cur_track, data_dict['track_record'], 0)

                        actual_wt = int(row['wt'])
                        declar_horse_wt = int(row['horse_wt_dec'])
                        dct_trend = source_datas.getValue(race_date_No, horse_code, data_dict['horse_dct_trend'], 0)
                        over_wt = row['over_wt'].strip()
                        current_rating = row['rtg']
                        if '-' in current_rating:
                            current_rating = 0
                        else:
                            current_rating = int(current_rating)
                        rating_trend = row['rtg_as'].strip()
                        if '-' == rating_trend:
                            rating_trend = 0
                        else:
                            rating_trend = int(rating_trend)

                        cls_standard_speed = source_datas.getValue(race_date_No, horse_code, data_dict['cls_standard_speed'], 0)

                        horse_best_recent_speed = source_datas.getValue(race_date_No, horse_code, data_dict['horse_best_recent_speed'], 0)
                        rest = source_datas.getValue(race_date_No, horse_code, data_dict['horse_rest'], 0)
                        pedigree_dst = source_datas.getValue(race_date_No, horse_code, data_dict['pedigree_dst'], False)
                        pedigree_track = False
                        fav_match = common.IsLowestOdds(win_odds, sort_history_raceResults_rows[race_date_No])
                        same_trainer_count = common.GetSameTrainerCount(trainer, sort_history_raceResults_rows[race_date_No])

                        odd_wave = source_datas.getHorseOddsWave(race_date_No, horse_code, data_dict['horse_odds_wave'])

                        item = (race_date, race_id, race_no, horse_no, pla_odds, win_odds, plc, horse_code, trainer,
                                jockey, site, going, course, dst, cls, draw, gear, horse_records[0], horse_records[1],
                                horse_recent_record[0],  horse_recent_record[1], horse_fav_record[0], horse_fav_record[1],
                                horse_site_course_record[0], horse_site_course_record[1], horse_site_course_fav_record[0],
                                horse_site_course_fav_record[1], horse_going_record[0], horse_going_record[1],
                                horse_dst_record[0], horse_dst_record[1], horse_cls_record[0], horse_cls_record[1],
                                horse_gear_record[0], horse_gear_record[1], horse_best_speed, lbw, finish_time,
                                trainer_record[0], trainer_record[1], trainer_recent[0], trainer_recent[1],
                                trainer_fav_record[0], trainer_fav_record[1], jockey_record[0], jockey_record[1],
                                jockey_recent[0], jockey_recent[1], jockey_fav_record[0], jockey_fav_record[1],
                                draw_record[0], draw_record[1], track_fav_record, track_record, actual_wt,
                                declar_horse_wt, dct_trend, over_wt, current_rating, rating_trend, cls_standard_speed,
                                horse_best_recent_speed, rest, pedigree_dst, pedigree_track, fav_match,
                                same_trainer_count, odd_wave)
                        all_list.append(item)

        export.export(all_list)
    else:
        pass



