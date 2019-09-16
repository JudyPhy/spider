from db.database import singleton_Results_DB
from config.myconfig import singleton_cfg

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
        sql = '''insert into {}(race_date, race_id, race_no, horse_no, pla_odds, win_odds, plc, 
         horse_code, trainer, jockey, site, going, course, dst, cls, draw, gear, horse_record_before4, 
        horse_record_total, horse_recent_before4,  horse_recent_total, horse_fav_record_before3, 
        horse_fav_record_total, horse_track_record_before4, horse_track_record_total, 
        horse_track_fav_record_before3, horse_track_fav_record_total, 
        horse_going_record_before4, horse_going_record_total, horse_dst_record_before4, 
        horse_dst_record_total, horse_cls_record_before4, horse_cls_record_total, 
        horse_gear_record_before4, horse_gear_record_total, horse_best_speed, lbw, finish_time,
        trainer_record_before4, trainer_record_total, trainer_recent_before4, trainer_recent_total,
        trainer_fav_record_before3, trainer_fav_record_total, jockey_record_before4, 
        jockey_record_total, jockey_recent_before4, jockey_recent_total, jockey_fav_record_before3, 
        jockey_fav_record_total, draw_record_before4, draw_record_total, track_fav_record_before3, 
        track_record_total, actual_wt, declar_horse_wt, dct_trend, over_wt, current_rating, rating_trend, 
        cls_standard_speed, horse_best_recent_speed, rest, pedigree_dst, pedigree_track, fav_match, 
        same_trainer_count, odd_wave, odd_diff) 
        values (%s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, 
        %s, %s, %s,          
        %s, %s,  
        %s, %s, %s, 
        %s, %s, %s,          
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, 
        %s, %s, %s,         
        %s, %s, %s, %s, 
        %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
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
    trainer VARCHAR(45) DEFAULT '',
    jockey VARCHAR(45) DEFAULT '',
    site VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',
    course VARCHAR(45) DEFAULT '',
    dst INT DEFAULT 0,
    cls VARCHAR(45) DEFAULT '',
    draw INT DEFAULT 0,
    gear VARCHAR(45) DEFAULT '',
    horse_record_before4 INT DEFAULT 0,
    horse_record_total INT DEFAULT 0,
    horse_recent_before4 INT DEFAULT 0,
    horse_recent_total INT DEFAULT 0,
    horse_fav_record_before3 INT DEFAULT 0,
    horse_fav_record_total INT DEFAULT 0,
    horse_track_record_before4 INT DEFAULT 0,
    horse_track_record_total INT DEFAULT 0,
    horse_track_fav_record_before3 INT DEFAULT 0,
    horse_track_fav_record_total INT DEFAULT 0,
    horse_going_record_before4 INT DEFAULT 0,
    horse_going_record_total INT DEFAULT 0,
    horse_dst_record_before4 INT DEFAULT 0,
    horse_dst_record_total INT DEFAULT 0,
    horse_cls_record_before4 INT DEFAULT 0,
    horse_cls_record_total INT DEFAULT 0,
    horse_gear_record_before4 INT DEFAULT 0,
    horse_gear_record_total INT DEFAULT 0,
    horse_best_speed FLOAT DEFAULT 0,
    lbw VARCHAR(45) DEFAULT '',
    finish_time INT DEFAULT 0,    
    trainer_record_before4 INT DEFAULT 0,
    trainer_record_total INT DEFAULT 0,
    trainer_recent_before4 INT DEFAULT 0,
    trainer_recent_total INT DEFAULT 0,
    trainer_fav_record_before3 INT DEFAULT 0,
    trainer_fav_record_total INT DEFAULT 0,
    jockey_record_before4 INT DEFAULT 0,
    jockey_record_total INT DEFAULT 0,
    jockey_recent_before4 INT DEFAULT 0,
    jockey_recent_total INT DEFAULT 0,    
    jockey_fav_record_before3 INT DEFAULT 0,
    jockey_fav_record_total INT DEFAULT 0,
    draw_record_before4 INT DEFAULT 0,
    draw_record_total INT DEFAULT 0,   
    track_fav_record_before3 INT DEFAULT 0,
    track_record_total INT DEFAULT 0,
    actual_wt INT DEFAULT 0,  
    declar_horse_wt INT DEFAULT 0,
    dct_trend INT DEFAULT 0,
    over_wt VARCHAR(45) DEFAULT '',
    current_rating INT DEFAULT 0, 
    rating_trend INT DEFAULT 0,  
    cls_standard_speed FLOAT DEFAULT 0,  
    horse_best_recent_speed FLOAT DEFAULT 0,
    rest INT DEFAULT 0,
    pedigree_dst INT DEFAULT 0,    
    pedigree_track INT DEFAULT 0,
    fav_match INT DEFAULT 0,
    same_trainer_count INT DEFAULT 0,
    odd_wave FLOAT DEFAULT 0,
    odd_diff FLOAT DEFAULT 0)'''.format(RESULT_TABLE)
    singleton_Results_DB.cursor.execute(sql)

