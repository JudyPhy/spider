### 根据合并表的数据，制作新结构的数据表 ###
from db import request_db_data
from common import common
from dragon import source_datas
from dragon import export
import datetime


def main():
    today = datetime.datetime.now()
    today_date = str(today.year) + common.toDoubleDigitStr(today.month) + common.toDoubleDigitStr(today.day)
    sort_history_raceCard_rows = request_db_data.RequestSortedHistoryRaceCardRows(today_date)  # race_date_No & {horse_code & row}
    sort_history_raceResults_rows = request_db_data.RequestSortedHistoryRaceResultsRows(today_date)  # race_date_No & {horse_code & row}
    horse_pedigree_rows = request_db_data.RequestHorsePedigreeRows()  # horse_code & row
    display_sectional_time_rows = request_db_data.RequestHistoryDisplaySectionalTimeRows(today_date)  # race_date_No & {horse_code & row}
    odds_sectional_rows = request_db_data.RequestSectionalOdds()  # race_date_No & {horse_No & row}
    if len(sort_history_raceCard_rows) > 0:
        data_dict = source_datas.prepareDatas(sort_history_raceCard_rows, sort_history_raceResults_rows, horse_pedigree_rows,
                                              display_sectional_time_rows, odds_sectional_rows)
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
                        trainer = row['trainer'].strip()
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
                        count_bucket = ''
                        odd_bucket = ''
                        pedigree_growth = False
                        pedigree_dst = source_datas.getValue(race_date_No, horse_code, data_dict['pedigree_dst'], False)
                        pedigree_track = False
                        horse_age = int(row['age'])

                        horse_records = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_record'])
                        horse_recent_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_recent_record'])
                        horse_site_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_site_record'])
                        horse_going_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_going_record'])
                        horse_course_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_course_record'])
                        horse_dst_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_dst_record'])
                        horse_cls_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_cls_record'])
                        horse_draw_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_draw_record'])
                        horse_jockey_record = source_datas.getRecords(race_date_No, horse_code, data_dict['horse_jockey_record'])

                        horse_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_speed'])
                        horse_recent_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_recent_speed'])
                        horse_site_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_site_speed'])
                        horse_going_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_going_speed'])
                        horse_course_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_course_speed'])
                        horse_dst_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_dst_speed'])
                        horse_cls_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_cls_speed'])
                        horse_draw_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_draw_speed'])
                        horse_gear_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_gear_speed'])
                        horse_jockey_speed = source_datas.getSpeeds(race_date_No, horse_code, data_dict['horse_jockey_speed'])

                        current_rating = row['rtg']
                        if '-' in current_rating:
                            current_rating = 0
                        else:
                            current_rating = int(current_rating)
                        declar_horse_wt = int(row['horse_wt_dec'])
                        actual_wt = int(row['wt'])
                        rating_trend = row['rtg_as']
                        if '-' == rating_trend:
                            rating_trend = 0
                        else:
                            rating_trend = int(rating_trend)

                        dct_trend = source_datas.getValue(race_date_No, horse_code, data_dict['horse_dct_trend'], 0)
                        act_trend = source_datas.getValue(race_date_No, horse_code, data_dict['horse_act_trend'], 0)
                        odd_trend = source_datas.getValue(race_date_No, horse_code, data_dict['horse_odds_trend'], 0)

                        rest = source_datas.getValue(race_date_No, horse_code, data_dict['horse_rest'], 0)
                        new_dis = source_datas.getValue(race_date_No, horse_code, data_dict['horse_new_dis'], False)

                        draw_record = source_datas.getRecords(race_date, draw, data_dict['draw_record'])
                        trainer_record = source_datas.getRecords(race_date, trainer, data_dict['trainer_record'])
                        jockey_record = source_datas.getRecords(race_date, jockey, data_dict['jockey_record'])
                        jockey_recent = source_datas.getRecords(race_date, jockey, data_dict['jockey_recent'])
                        jockey_trainer_record = source_datas.getRecords(race_date, jockey + '__' + trainer, data_dict['jockey_trainer_record'])

                        horse_last_dst_time = source_datas.getValue(race_date_No, horse_code, data_dict['horse_last_dst_time'], [0, 0, 0])
                        jockey_hot = source_datas.getValue(race_date_No, horse_code, data_dict['jockey_hot'], [0, 0])
                        odd_sectional_trend = source_datas.getHorseOddsSectionalTrend(race_date_No, horse_code, data_dict['horse_odds_sectional_trend'])

                        item = (race_date, race_id, race_no, horse_no, pla_odds, win_odds, plc, horse_code, trainer,
                                jockey, site, going, course, dst, cls, draw, gear, count_bucket, odd_bucket,
                                pedigree_growth,pedigree_dst, pedigree_track, horse_age, horse_records[0],
                                horse_records[1], horse_recent_record[0],  horse_recent_record[1], horse_site_record[0],
                                horse_site_record[1], horse_going_record[0], horse_going_record[1],
                                horse_course_record[0], horse_course_record[1], horse_dst_record[0], horse_dst_record[1],
                                horse_cls_record[0], horse_cls_record[1], horse_draw_record[0], horse_draw_record[1],
                                horse_jockey_record[0], horse_jockey_record[1], horse_speed[0], horse_speed[1],
                                horse_speed[2], horse_recent_speed[0], horse_recent_speed[1], horse_recent_speed[2],
                                horse_site_speed[0], horse_site_speed[1], horse_site_speed[2], horse_going_speed[0],
                                horse_going_speed[1], horse_going_speed[2], horse_course_speed[0], horse_course_speed[1],
                                horse_course_speed[2], horse_dst_speed[0], horse_dst_speed[1], horse_dst_speed[2],
                                horse_cls_speed[0], horse_cls_speed[1], horse_cls_speed[2], horse_draw_speed[0],
                                horse_draw_speed[1], horse_draw_speed[2], horse_gear_speed[0], horse_gear_speed[1],
                                horse_gear_speed[2], horse_jockey_speed[0], horse_jockey_speed[1], horse_jockey_speed[2],
                                current_rating, declar_horse_wt, actual_wt, rating_trend, dct_trend, act_trend,
                                odd_trend, rest, new_dis, draw_record[0], draw_record[1], trainer_record[0],
                                trainer_record[1], jockey_record[0], jockey_record[1], jockey_recent[0], jockey_recent[1],
                                jockey_trainer_record[0], jockey_trainer_record[1], horse_last_dst_time[0],
                                horse_last_dst_time[1], horse_last_dst_time[2], jockey_hot[0], jockey_hot[1],
                                odd_sectional_trend)
                        all_list.append(item)

        export.export(all_list)
    else:
        pass



