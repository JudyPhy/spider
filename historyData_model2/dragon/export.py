from db.database import singleton_Results_DB
from config.myconfig import singleton_cfg

# 结果存储表名
RESULT_TABLE = singleton_cfg.getDragonExportTable()


def export(all_list):
    if singleton_Results_DB.table_exists(RESULT_TABLE):
        singleton_Results_DB.cursor.execute('drop table {}'.format(RESULT_TABLE))
        singleton_Results_DB.connect.commit()
    __insert(all_list)


def __insert(all_list):
    __createNewTable()
    sql = '''insert into {}(race_date, race_id, horse_code, horse_no, pla_odds, win_odds, plc, count, race_no, site, cls,
            distance, bonus, going, course, actual_wt, declar_horse_wt, draw,
            current_rating, season_stakes, total_stakes, horse_age, 
            horse_star_0_curRace, horse_star_1_curRace, horse_star_2_curRace, horse_star_3_curRace, horse_total_curRace,
            horse_star_0_allRace, horse_star_1_allRace, horse_star_2_allRace, horse_star_3_allRace, horse_total_allRace,
            raceDays, score, pre_race_speed, race_speed, dis_avesr, dis_avesr_horse, go_aversr, go_aversr_horse,
            new_dis, rest, act_delta, dct_delta, jt_raceCount, jt_raceCount_before3, hj_raceCount, hj_raceCount_before3, 
            ht_raceCount, ht_raceCount_before3)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(RESULT_TABLE)
    singleton_Results_DB.cursor.executemany(sql, all_list)
    singleton_Results_DB.connect.commit()


def __createNewTable():
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date INT DEFAULT 0,
    raceDays INT DEFAULT 0,
    race_id BIGINT DEFAULT 0,
    horse_code VARCHAR(45) DEFAULT '',
    horse_no INT DEFAULT 0,
    pla_odds FLOAT DEFAULT 0.0,
    win_odds FLOAT DEFAULT 0.0,
    score INT DEFAULT 0,
    plc INT DEFAULT 0,
    declar_horse_wt INT DEFAULT 0,
    current_rating INT DEFAULT 0,
    total_stakes INT DEFAULT 0,
    count INT DEFAULT 0,
    race_no INT DEFAULT 0,
    cls VARCHAR(45) DEFAULT '',
    distance INT DEFAULT 0,
    bonus INT DEFAULT 0,
    actual_wt INT DEFAULT 0,
    draw INT DEFAULT 0,
    season_stakes INT DEFAULT 0,
    horse_age INT DEFAULT 0,
    horse_star_0_curRace INT DEFAULT 0,
    horse_star_1_curRace INT DEFAULT 0,
    horse_star_2_curRace INT DEFAULT 0,
    horse_star_3_curRace INT DEFAULT 0,
    horse_total_curRace INT DEFAULT 0,
    horse_star_0_allRace INT DEFAULT 0,
    horse_star_1_allRace INT DEFAULT 0,
    horse_star_2_allRace INT DEFAULT 0,
    horse_star_3_allRace INT DEFAULT 0,
    horse_total_allRace INT DEFAULT 0,
    site VARCHAR(45) DEFAULT '',
    going VARCHAR(45) DEFAULT '',
    course VARCHAR(45) DEFAULT '',
    pre_race_speed FLOAT DEFAULT 0,
    race_speed FLOAT DEFAULT 0,
    dis_avesr FLOAT DEFAULT 0,
    dis_avesr_horse FLOAT DEFAULT 0,
    go_aversr FLOAT DEFAULT 0,
    go_aversr_horse FLOAT DEFAULT 0,
    new_dis INT DEFAULT 0,
    rest INT DEFAULT 0,
    act_delta INT DEFAULT 0,
    dct_delta INT DEFAULT 0,
    jt_raceCount INT DEFAULT 0,
    jt_raceCount_before3 INT DEFAULT 0,
    hj_raceCount INT DEFAULT 0,
    hj_raceCount_before3 INT DEFAULT 0,
    ht_raceCount INT DEFAULT 0,
    ht_raceCount_before3 INT DEFAULT 0)'''.format(RESULT_TABLE)
    singleton_Results_DB.cursor.execute(sql)

