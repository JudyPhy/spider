from db.database import singleton_Results_DB
from config.myconfig import singleton_cfg

# ����洢����
RESULT_TABLE = singleton_cfg.getDragonExportTable()


def export(all_list):
    if singleton_Results_DB.table_exists(RESULT_TABLE):
        singleton_Results_DB.cursor.execute('drop table {}'.format(RESULT_TABLE))
        singleton_Results_DB.connect.commit()
    __insert(all_list)


def __insert(all_list):
    __createNewTable()
    try:
        singleton_Results_DB.cursor.execute('delete from {} where race_date=%s'.format(RESULT_TABLE), singleton_cfg.getRaceDate())
        sql = '''insert into {}(race_date, race_id, race_no, horse_no, pla_odds, win_odds, plc, horse_code, trainer_code, jockey_code,
        site_label, going, course_label, dst_label, cls_label, draw_label, gear_label, count_bucket, odd_bucket, pedigree_growth,
        pedigree_dst, pedigree_track, horse_age, 
        horse_record_before4, horse_record_total, 
        horse_recent_record_before4, horse_recent_record_total, 
        horse_site_record_before4, horse_site_record_total,
        horse_go_record_before4, horse_go_record_total,
        horse_course_record_before4, horse_course_record_total,
        horse_dst_record_before4, horse_dst_record_total,
        horse_cls_record_before4, horse_cls_record_total,
        horse_draw_record_before4, horse_draw_record_total,
        horse_jockey_record_before4, horse_jockey_record_total,
        horse_best_speed, horse_lowest_speed, horse_avr_speed,
        horse_recent_best_speed, horse_recent_lowest_speed, horse_recent_avr_speed,
        horse_site_best_speed, horse_site_lowest_speed, horse_site_avr_speed,
        horse_go_best_speed, horse_go_lowest_speed, horse_go_avr_speed,
        horse_course_best_speed, horse_course_lowest_speed, horse_course_avr_speed,
        horse_dst_best_speed, horse_dst_lowest_speed, horse_dst_avr_speed,
        horse_cls_best_speed, horse_cls_lowest_speed, horse_cls_avr_speed,
        horse_draw_best_speed, horse_draw_lowest_speed, horse_draw_avr_speed,
        horse_gear_best_speed, horse_gear_lowest_speed, horse_gear_avr_speed,
        horse_jockey_best_speed, horse_jockey_lowest_speed, horse_jockey_avr_speed,
        current_rating, declar_horse_wt, actual_wt, rating_trend, dct_trend, act_trend, odd_trend, rest, new_dis,
        draw_record_before4, draw_record_total,
        trainer_record_before4, trainer_record_total,
        jockey_record_before4, jockey_record_total,
        jockey_recent_before4, jockey_recent_total,
        horse_last_dst_time_prev, horse_last_dst_time_ave,
        jockey_hot, jockey_hot_before4, odd_wave) 
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, 
        %s, %s, 
        %s, %s, 
        %s, %s, 
        %s, %s,
        %s, %s, 
        %s, %s,
        %s, %s, 
        %s, %s, 
        %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, 
        %s, %s, 
        %s, %s,
        %s, %s,
        %s, %s, 
        %s, %s, %s)'''.format(RESULT_TABLE)
        singleton_Results_DB.cursor.executemany(sql, all_list)
        singleton_Results_DB.connect.commit()
    except Exception as error:
        print(error)


def __createNewTable():
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date INT DEFAULT 0,
    race_id INT DEFAULT 0,
    race_no INT DEFAULT 0,
    horse_no INT DEFAULT 0,
    pla_odds FLOAT DEFAULT 0.0,
    win_odds FLOAT DEFAULT 0.0,
    plc INT DEFAULT 0,
    horse_code VARCHAR(45) DEFAULT '',
    trainer_code VARCHAR(45) DEFAULT '',
    jockey_code VARCHAR(45) DEFAULT '',
    site_label VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',
    course_label VARCHAR(45) DEFAULT '',
    dst_label INT DEFAULT 0,
    cls_label VARCHAR(45) DEFAULT '',
    draw_label INT DEFAULT 0,
    gear_label VARCHAR(45) DEFAULT '',
    count_bucket VARCHAR(45) DEFAULT '',
    odd_bucket VARCHAR(45) DEFAULT '',
    pedigree_growth INT DEFAULT 0,
    pedigree_dst INT DEFAULT 0,
    pedigree_track INT DEFAULT 0,
    horse_age INT DEFAULT 0,
    horse_record_before4 INT DEFAULT 0,
    horse_record_total INT DEFAULT 0,
    horse_recent_record_before4 INT DEFAULT 0,
    horse_recent_record_total INT DEFAULT 0,
    horse_site_record_before4 INT DEFAULT 0,
    horse_site_record_total INT DEFAULT 0,
    horse_go_record_before4 INT DEFAULT 0,
    horse_go_record_total INT DEFAULT 0,
    horse_course_record_before4 INT DEFAULT 0,
    horse_course_record_total INT DEFAULT 0,
    horse_dst_record_before4 INT DEFAULT 0,
    horse_dst_record_total INT DEFAULT 0,
    horse_cls_record_before4 INT DEFAULT 0,
    horse_cls_record_total INT DEFAULT 0,
    horse_draw_record_before4 INT DEFAULT 0,
    horse_draw_record_total INT DEFAULT 0,
    horse_jockey_record_before4 INT DEFAULT 0,
    horse_jockey_record_total INT DEFAULT 0,
    horse_best_speed FLOAT DEFAULT 0,
    horse_lowest_speed FLOAT DEFAULT 0,
    horse_avr_speed FLOAT DEFAULT 0,
    horse_recent_best_speed FLOAT DEFAULT 0,
    horse_recent_lowest_speed FLOAT DEFAULT 0,
    horse_recent_avr_speed FLOAT DEFAULT 0,
    horse_site_best_speed FLOAT DEFAULT 0,
    horse_site_lowest_speed FLOAT DEFAULT 0,
    horse_site_avr_speed FLOAT DEFAULT 0,
    horse_go_best_speed FLOAT DEFAULT 0,
    horse_go_lowest_speed FLOAT DEFAULT 0,
    horse_go_avr_speed FLOAT DEFAULT 0,
    horse_course_best_speed FLOAT DEFAULT 0,
    horse_course_lowest_speed FLOAT DEFAULT 0,
    horse_course_avr_speed FLOAT DEFAULT 0,
    horse_dst_best_speed FLOAT DEFAULT 0,
    horse_dst_lowest_speed FLOAT DEFAULT 0,
    horse_dst_avr_speed FLOAT DEFAULT 0,
    horse_cls_best_speed FLOAT DEFAULT 0,
    horse_cls_lowest_speed FLOAT DEFAULT 0,
    horse_cls_avr_speed FLOAT DEFAULT 0,
    horse_draw_best_speed FLOAT DEFAULT 0,
    horse_draw_lowest_speed FLOAT DEFAULT 0,
    horse_draw_avr_speed FLOAT DEFAULT 0,
    horse_gear_best_speed FLOAT DEFAULT 0,
    horse_gear_lowest_speed FLOAT DEFAULT 0,
    horse_gear_avr_speed FLOAT DEFAULT 0,
    horse_jockey_best_speed FLOAT DEFAULT 0,
    horse_jockey_lowest_speed FLOAT DEFAULT 0,
    horse_jockey_avr_speed FLOAT DEFAULT 0,
    current_rating INT DEFAULT 0,    
    declar_horse_wt INT DEFAULT 0,  
    actual_wt INT DEFAULT 0,
    rating_trend INT DEFAULT 0,
    dct_trend INT DEFAULT 0,
    act_trend INT DEFAULT 0,
    odd_trend INT DEFAULT 0,
    rest INT DEFAULT 0,
    new_dis INT DEFAULT 0,
    draw_record_before4 INT DEFAULT 0,
    draw_record_total INT DEFAULT 0,
    trainer_record_before4 INT DEFAULT 0,
    trainer_record_total INT DEFAULT 0,
    jockey_record_before4 INT DEFAULT 0,
    jockey_record_total INT DEFAULT 0,
    jockey_recent_before4 INT DEFAULT 0,
    jockey_recent_total INT DEFAULT 0,
    horse_last_dst_time_prev FLOAT DEFAULT 0,
    horse_last_dst_time_ave FLOAT DEFAULT 0,
    jockey_hot INT DEFAULT 0,
    jockey_hot_before4 INT DEFAULT 0,
    odd_wave FLOAT DEFAULT 0)'''.format(RESULT_TABLE)
    singleton_Results_DB.cursor.execute(sql)

