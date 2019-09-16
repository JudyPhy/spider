from dragon import source_datas
from dragon import export
from config.myconfig import singleton_cfg
from db import request_db_data
from common import common


def main():
    today_date = singleton_cfg.getRaceDate()
    print('Today=>', today_date)
    immd_info_dict = request_db_data.RequestImmdLatestRows(today_date)  # race_date_No & {horse_No & row}
    future_raceCard_rows = request_db_data.RequestFutureRaceCardRows(today_date)    # race_date_No & {horse_No & row}
    history_raceCard_rows = request_db_data.RequestHistoryRaceCardRows(today_date)  # race_date_No & {horse_code & row}
    history_raceResults_rows = request_db_data.RequestHistoryRaceResultsRows(today_date)    # race_date_No & {horse_code & row}
    horse_pedigree_rows = request_db_data.RequestHorsePedigreeRows()    # horse_code & row
    # display_sectional_time_rows = request_db_data.RequestHistoryDisplaySectionalTimeRows(today_date)  # race_date_No & {horse_code & row}
    course_standard_times_rows = request_db_data.RequestCourseStandardTimes()  # race_date_No & {horse_No & row}
    if len(future_raceCard_rows) > 0:
        data_dict = source_datas.prepareDatas(future_raceCard_rows, immd_info_dict, history_raceResults_rows,
                                              history_raceCard_rows, horse_pedigree_rows)
        all_list = []
        for race_date_No, dict in future_raceCard_rows.items():
            for horse_No, row in dict.items():
                race_date = row['race_date']
                race_No = row['race_No']
                horse_code = row['horse_code'].strip()
                trainer = source_datas.getTrainer(race_date_No, horse_No, immd_info_dict, row)
                jockey = source_datas.getJockey(race_date_No, horse_No, immd_info_dict, row)
                site = row['site'].replace(' ', '')
                going = data_dict['going'][race_date_No]
                course = source_datas.getCourse(row['course'])
                dst = int(row['distance'])
                cls = row['cls'].strip()
                draw = int(row['draw'])
                gear = row['gear'].strip()

                horse_records = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_record'])
                horse_recent_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_recent_record'])
                horse_fav_record = source_datas.getHorseFavRecords(race_date_No, horse_No, data_dict['horse_fav_record'])
                horse_site_course_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_site_course_record'])
                horse_site_course_fav_record = source_datas.getHorseFavRecords(race_date_No, horse_No, data_dict['horse_site_course_fav_record'])
                horse_going_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_go_record'])
                horse_dst_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_dst_record'])
                horse_cls_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_cls_record'])
                horse_gear_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_gear_record'])

                best_time = row['best_time'].strip()
                if best_time == '':
                    horse_best_speed = 0
                else:
                    horse_best_speed = dst/common.GetTotalSeconds(best_time)
                lbw = ''
                finish_time = 0

                trainer_record = source_datas.getRecords(trainer, data_dict['trainer_record'])
                trainer_recent = source_datas.getRecords(trainer, data_dict['trainer_recent'])
                trainer_fav_record = source_datas.getFavRecords(trainer, data_dict['trainer_fav_record'])

                jockey_record = source_datas.getRecords(jockey, data_dict['jockey_record'])
                jockey_recent = source_datas.getRecords(jockey, data_dict['jockey_recent'])
                jockey_fav_record = source_datas.getFavRecords(jockey, data_dict['jockey_fav_record'])

                draw_record = source_datas.getRecords(draw, data_dict['draw_record'])
                cur_track = site + '_' + course.upper()
                track_fav_record = source_datas.getPedigreeDst(cur_track, data_dict['track_fav_record'], 0)
                track_record = source_datas.getPedigreeDst(cur_track, data_dict['track_record'], 0)

                actual_wt = int(row['wt'])
                if row['horse_wt_dec'] == '':
                    declar_horse_wt = 1200
                else:
                    declar_horse_wt = int(row['horse_wt_dec'])
                dct_trend = source_datas.getValue(race_date_No, horse_No, data_dict['horse_dct_trend'], 0)
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

                cls_standard_speed = source_datas.getClsStandardSpeed(site, row['course'], dst, cls, course_standard_times_rows)

                horse_best_recent_speed = source_datas.getValue(race_date_No, horse_No, data_dict['horse_best_recent_speed'], 0)
                rest = source_datas.getValue(race_date_No, horse_No, data_dict['horse_rest'], 0)
                pedigree_dst = source_datas.getPedigreeDst(horse_code, data_dict['pedigree_dst'], False)
                pedigree_track = False
                fav_match = False
                same_trainer_count = common.GetSameTrainerCount(trainer, dict)

                odd_wave = 1
                odd_diff = 0

                item = (race_date, race_No, race_No, horse_No, 1, 1, 999, horse_code, trainer,
                        jockey, site, going, course, dst, cls, draw, gear, horse_records[0], horse_records[1],
                        horse_recent_record[0],  horse_recent_record[1], horse_fav_record[0], horse_fav_record[1],
                        horse_site_course_record[0], horse_site_course_record[1], horse_site_course_fav_record[0],
                        horse_site_course_fav_record[1], horse_going_record[0], horse_going_record[1],
                        horse_dst_record[0], horse_dst_record[1], horse_cls_record[0], horse_cls_record[1],
                        horse_gear_record[0], horse_gear_record[1], horse_best_speed, lbw, finish_time,
                        trainer_record[0], trainer_record[1], trainer_recent[0], trainer_recent[1],
                        trainer_fav_record[0], trainer_fav_record[1], jockey_record[0], jockey_record[1],
                        jockey_recent[0], jockey_recent[1], jockey_fav_record[0], jockey_fav_record[1],
                        draw_record[0], draw_record[1], track_fav_record, track_record, actual_wt, declar_horse_wt,
                        dct_trend, over_wt, current_rating, rating_trend, cls_standard_speed, horse_best_recent_speed,
                        rest, pedigree_dst, pedigree_track, fav_match, same_trainer_count, odd_wave, odd_diff)
                all_list.append(item)
        export.export(all_list)
    else:
        pass



