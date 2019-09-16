from dragon import source_datas
from dragon import export
from config.myconfig import singleton_cfg
from db import request_db_data


def main():
    today_date = singleton_cfg.getRaceDate()
    print('Today=>', today_date)
    immd_info_dict = request_db_data.RequestImmdLatestRows(today_date)  # race_date_No & {horse_No & row}
    future_raceCard_rows = request_db_data.RequestFutureRaceCardRows(today_date)    # race_date_No & {horse_No & row}
    history_raceCard_rows = request_db_data.RequestHistoryRaceCardRows(today_date)  # race_date_No & {horse_code & row}
    history_raceResults_rows = request_db_data.RequestHistoryRaceResultsRows(today_date)    # race_date_No & {horse_code & row}
    horse_pedigree_rows = request_db_data.RequestHorsePedigreeRows()    # horse_code & row
    display_sectional_time_rows = request_db_data.RequestHistoryDisplaySectionalTimeRows(today_date)  # race_date_No & {horse_code & row}
    if len(future_raceCard_rows) > 0:
        data_dict = source_datas.prepareDatas(future_raceCard_rows, immd_info_dict, history_raceResults_rows,
                                              history_raceCard_rows, horse_pedigree_rows, display_sectional_time_rows)
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
                count_bucket = ''
                odd_bucket = ''
                pedigree_growth = False
                pedigree_dst = source_datas.getValue(race_date_No, horse_No, data_dict['pedigree_dst'], False)
                pedigree_track = False
                horse_age = int(row['age'])

                horse_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_record'])
                horse_recent_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_recent_record'])
                horse_site_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_site_record'])
                horse_go_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_go_record'])
                horse_course_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_course_record'])
                horse_dst_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_dst_record'])
                horse_cls_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_cls_record'])
                horse_draw_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_draw_record'])
                horse_jockey_record = source_datas.getHorseRecords(race_date_No, horse_No, data_dict['horse_jockey_record'])

                horse_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_speed'])
                horse_recent_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_recent_speed'])
                horse_site_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_site_speed'])
                horse_go_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_go_speed'])
                horse_course_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_course_speed'])
                horse_dst_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_dst_speed'])
                horse_cls_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_cls_speed'])
                horse_draw_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_draw_speed'])
                horse_gear_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_gear_speed'])
                horse_jockey_speed = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_jockey_speed'])
                horse_last_dst_time = source_datas.getHorseSpeeds(race_date_No, horse_No, data_dict['horse_last_dst_time'])

                current_rating = source_datas.getValue(race_date_No, horse_No, data_dict['rtg'], -1)
                if row['horse_wt_dec'] == '':
                    declar_horse_wt = 1200
                else:
                    declar_horse_wt = int(row['horse_wt_dec'])
                actual_wt = int(row['wt'])

                rating_trend = source_datas.getRatingTrend(row['rtg_as'])
                dct_trend = source_datas.getValue(race_date_No, horse_No, data_dict['horse_dct_trend'], -1)
                act_trend = source_datas.getValue(race_date_No, horse_No, data_dict['horse_act_trend'], -1)
                odd_trend = 0
                odd_sectional_trend = 1

                rest = source_datas.getValue(race_date_No, horse_No, data_dict['horse_rest'], -1)
                new_dis = source_datas.getValue(race_date_No, horse_No, data_dict['horse_new_dis'], False)

                draw_record = source_datas.getRecords(draw, data_dict['draw_record'])
                trainer_record = source_datas.getRecords(trainer, data_dict['trainer_record'])
                jockey_record = source_datas.getRecords(jockey, data_dict['jockey_record'])
                jockey_recent = source_datas.getRecords(jockey, data_dict['jockey_recent'])
                jockey_trainer_record = source_datas.getRecords(jockey + '__' + trainer, data_dict['jockey_trainer_record'])

                jockey_hot = source_datas.getHot(jockey, data_dict['jockey_hot'])

                item = (race_date, race_No, race_No, horse_No, 1, 1, 999, horse_code, trainer, jockey, site, going, course,
                        dst, cls, draw, gear, count_bucket, odd_bucket, pedigree_growth, pedigree_dst, pedigree_track,
                        horse_age, horse_record[0], horse_record[1], horse_recent_record[0], horse_recent_record[1],
                        horse_site_record[0], horse_site_record[1], horse_go_record[0], horse_go_record[1],
                        horse_course_record[0], horse_course_record[1], horse_dst_record[0], horse_dst_record[1],
                        horse_cls_record[0], horse_cls_record[1], horse_draw_record[0], horse_draw_record[1],
                        horse_jockey_record[0], horse_jockey_record[1], horse_speed[0], horse_speed[1], horse_speed[2],
                        horse_recent_speed[0], horse_recent_speed[1], horse_recent_speed[2], horse_site_speed[0],
                        horse_site_speed[1], horse_site_speed[2], horse_go_speed[0], horse_go_speed[1], horse_go_speed[2],
                        horse_course_speed[0], horse_course_speed[1], horse_course_speed[2], horse_dst_speed[0],
                        horse_dst_speed[1], horse_dst_speed[2], horse_cls_speed[0], horse_cls_speed[1], horse_cls_speed[2],
                        horse_draw_speed[0], horse_draw_speed[1], horse_draw_speed[2], horse_gear_speed[0],
                        horse_gear_speed[1], horse_gear_speed[2], horse_jockey_speed[0], horse_jockey_speed[1],
                        horse_jockey_speed[2], current_rating, declar_horse_wt, actual_wt, rating_trend, dct_trend,
                        act_trend, odd_trend, rest, new_dis, draw_record[0], draw_record[1], trainer_record[0],
                        trainer_record[1], jockey_record[0], jockey_record[1], jockey_recent[0], jockey_recent[1],
                        jockey_trainer_record[0], jockey_trainer_record[1], horse_last_dst_time[0], horse_last_dst_time[1],
                        horse_last_dst_time[2], jockey_hot[0], jockey_hot[1], odd_sectional_trend)
                all_list.append(item)

        export.export(all_list)
    else:
        pass



