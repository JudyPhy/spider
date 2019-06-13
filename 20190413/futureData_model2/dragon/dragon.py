### 根据合并表的数据，制作新结构的数据表 ###
from db.database import singleton_Scrub_DB
from common import common
from config.myconfig import singleton_cfg
from dragon import source_datas
from dragon import export


# 获取当天比赛数据
def __searchTodayRaceData():
    today_rows = []
    today_date = singleton_cfg.getRaceDate()
    tableName = singleton_cfg.getFutureRaceCardTable()
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {} where race_date=%s'.format(tableName), today_date)
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            if '(Withdrawn)' not in row['horse']:
                today_rows.append(row)
            else:
                print(row)
    else:
        common.log('dragon: Table[' + tableName + '] not exist.')
    return today_rows


# 将原数据转成目标数据结构
def __toTargetStruct(row, count, horse_info, horse_age, horse_starts, horse_score, horse_speed, season_stakes, current_rating,
                     horse_deltaDays, dis_ave_speed, dis_ave_horse_speed, go_ave_speed, go_ave_horse_speed, new_dis,
                     rest, act_delta, dct_delta, hj_raceCount, ht_raceCount, jt_raceCount):
    race_date = row['race_date']
    race_id = row['race_No']
    horse_code = row['horse_code']
    horse_no = row['horse_No']
    pla_odds = 1
    win_odds = 1
    plc = 999

    race_no = row['race_No']
    site = row['site'].replace(' ', '')
    cls = row['cls'].replace(' ', '').replace('Class', '').strip()
    distance = int(row['distance'])
    bonus = row['bonus']
    going = row['going'].replace(' ', '').strip().upper()
    if going == '':
        going = 'GOOD'

    array_course = row['course'].split('"')
    if len(array_course) == 3:
        course = array_course[1].strip().upper()
    else:
        course = row['course'].strip().upper()

    actual_wt = row['wt']

    if (row['horse_wt_dec'] == '') or ('\xa0' in row['horse_wt_dec']):
        declar_horse_wt = 0
    elif '-' in row['horse_wt_dec']:
        declar_horse_wt = -999
    else:
        declar_horse_wt = int(row['horse_wt_dec'])

    if ('-' in row['draw']) or ('\xa0' in row['draw']):
        draw = 0
    else:
        draw = int(row['draw'])

    total_stakes = horse_info['total_stakes']

    horse_star_0_curRace = horse_starts['No1_curRace']
    horse_star_1_curRace = horse_starts['No2_curRace']
    horse_star_2_curRace = horse_starts['No3_curRace']
    horse_star_3_curRace = horse_starts['No4_curRace']
    horse_total_curRace = horse_starts['Total_curRace']
    horse_star_0_allRace = horse_starts['No1_allRace']
    horse_star_1_allRace = horse_starts['No2_allRace']
    horse_star_2_allRace = horse_starts['No3_allRace']
    horse_star_3_allRace = horse_starts['No4_allRace']
    horse_total_allRace = horse_starts['Total_allRace']

    if '-' in row['rtg']:
        rtg = 0
    else:
        rtg = int(row['rtg'])

    item = (race_date, race_id, horse_code, horse_no, pla_odds, win_odds, plc, count, race_no, site, cls, distance, bonus, going,
            course, actual_wt, declar_horse_wt, draw, rtg, season_stakes, total_stakes, horse_age,
            horse_star_0_curRace, horse_star_1_curRace, horse_star_2_curRace, horse_star_3_curRace, horse_total_curRace,
            horse_star_0_allRace, horse_star_1_allRace, horse_star_2_allRace, horse_star_3_allRace, horse_total_allRace,
            horse_deltaDays, horse_score, horse_speed[0], horse_speed[1], dis_ave_speed, dis_ave_horse_speed,
            go_ave_speed, go_ave_horse_speed, new_dis, rest, act_delta, dct_delta, hj_raceCount[0], hj_raceCount[1],
            ht_raceCount[0], ht_raceCount[1], jt_raceCount[0], jt_raceCount[1])
    return item


def main():
    all_list = []

    # 当天数据
    today_race_list = __searchTodayRaceData()
    if len(today_race_list) > 0:
        data_dict = source_datas.prepareDatas(today_race_list)
        for row in today_race_list:
            horse_code = row['horse_code']
            # horse info
            horse_info = source_datas.getHorseInfo(row, data_dict['horse_detail'])
            # race count
            race_count = source_datas.getRaceCount(row, data_dict['race_count'])
            # horse starts
            horse_starts = source_datas.getHorseStartsInfo(row, data_dict['horse_raceStarts'])
            # horse deltaDays
            horse_deltaDays = source_datas.getHorseDate(horse_code, data_dict['horse_deltaDays'], 0)
            # horse score
            horse_score = source_datas.getHorseDate(horse_code, data_dict['horse_score'], 1500)
            # horse age
            # horse_age = source_datas.getHorseDate(horse_code, data_dict['horse_age'], 3)
            horse_age = row['age']
            # horse speed
            horse_speed = source_datas.getHorseSpeed(row, data_dict['horse_speed'])
            # current rating before
            current_rating = source_datas.getCurrentRating(row, data_dict['current_rating'])
            # season stakes before
            season_stakes = source_datas.getHorseDate(horse_code, data_dict['season_stakes'], 0)
            # dis_ave_speed
            dis_ave_speed = source_datas.getHorseDate(int(row['distance']), data_dict['dis_avesr'], 0)
            # dis_ave_horse_speed
            dis_ave_horse_speed = source_datas.getHorseDate(horse_code, data_dict['dis_avesr_horse'], 0)
            # go_ave_speed
            going = row['going'].replace(' ', '').upper()
            if going == '':
                going = 'GOOD'
            go_ave_speed = source_datas.getHorseDate(going, data_dict['go_aversr'], 0)
            # go_ave_horse_speed
            go_ave_horse_speed = source_datas.getHorseDate(horse_code, data_dict['go_aversr_horse'], 0)
            # new_dis
            new_dis = source_datas.getNewDisData(horse_code, data_dict['horse_newDis'], 'new_dis', False)
            # rest
            rest = source_datas.getNewDisData(horse_code, data_dict['horse_newDis'], 'rest', 0)
            # act_delta
            act_delta = source_datas.getNewDisData(horse_code, data_dict['horse_newDis'], 'act_delta', 0)
            # dct_delta
            dct_delta = source_datas.getNewDisData(horse_code, data_dict['horse_newDis'], 'dct_delta', 0)
            # hj_raceCount
            array_jockey = row['jockey'].split('(')
            hj = row['horse_code'].strip() + '__' + array_jockey[0].strip()
            hj_raceCount = source_datas.getHorseDate(hj, data_dict['hj_raceCount'], [0, 0])
            # ht_raceCount
            array_trainer = row['trainer'].split('(')
            ht = row['horse_code'].strip() + '__' + array_trainer[0].strip()
            ht_raceCount = source_datas.getHorseDate(ht, data_dict['ht_raceCount'], [0, 0])
            # jt_raceCount
            jt = array_jockey[0].strip() + '__' + array_trainer[0].strip()
            jt_raceCount = source_datas.getHorseDate(jt, data_dict['jt_raceCount'], [0, 0])
            # 将数据组装成目标数据结构
            cur_row = __toTargetStruct(row, race_count, horse_info, horse_age, horse_starts,
                                       horse_score, horse_speed, season_stakes, current_rating, horse_deltaDays, dis_ave_speed, dis_ave_horse_speed,
                                       go_ave_speed, go_ave_horse_speed, new_dis, rest, act_delta, dct_delta, hj_raceCount,
                                       ht_raceCount, jt_raceCount)
            item = (cur_row)
            all_list.append(item)

        export.export(all_list)
    else:
        pass



