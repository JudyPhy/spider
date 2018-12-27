### 根据合并表的数据，制作新结构的数据表 ###
from db.database import singleton_Results_DB
from common import common
from config.myconfig import singleton_cfg
from dragon import source_datas
from dragon import export

RESULTS_FROM_TABLE = singleton_cfg.getCombineResultsExportTable()
HORSE_FROM_TABLE = singleton_cfg.getCombineHorseExportTable()


def __searchAllResultsData():
    rows = []
    if singleton_Results_DB.table_exists(RESULTS_FROM_TABLE):
        singleton_Results_DB.cursor.execute('select * from {}'.format(RESULTS_FROM_TABLE))
        rows = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
    else:
        common.log('dragon: Table[' + RESULTS_FROM_TABLE + '] not exist.')
    return rows


def __searchAllHorse():
    all_info = {}   # horse_code & row
    if singleton_Results_DB.table_exists(HORSE_FROM_TABLE):
        singleton_Results_DB.cursor.execute("select code,current_rating,season_stakes,total_stakes from {}".format(HORSE_FROM_TABLE))
        all_list = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in all_list:
            key = row['code'].strip()
            if key not in all_info.keys():
                all_info[key] = row
            else:
                common.log('has repeat horse in all_origin_results_data, code=' + key)
    else:
        common.log('dragon: Table[' + HORSE_FROM_TABLE + '] not exist.')
    return all_info


# 将原数据转成目标数据结构
def __toTargetStruct(row, count, horse_info, horse_age, horse_starts, horse_score, horse_speed, current_rating,
                     horse_deltaDays, dis_ave_speed, go_ave_speed, new_dis_array):
    race_date = row['race_date']
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_no = row['horse_No']
    pla_odds = 1
    win_odds = row['win_odds']

    if row['plc'] in common.words:
        plc = -1
    elif 'DH' in row['plc']:
        plc = int(row['plc'].replace('DH', ''))
    else:
        plc = int(row['plc'])

    race_no = row['race_No']
    site = row['site'].replace(' ', '')
    cls = row['cls'].replace('Class', '').strip()
    distance = int(row['distance'])
    bonus = row['bonus']
    going = row['going'].replace(' ', '').strip().upper()
    if going == '':
        going = 'GOOD'

    array_course = row['course'].split('"')
    if len(array_course) == 3:
        course = array_course[1]
    else:
        course = row['course']

    actual_wt = row['actual_wt']

    if row['declar_horse_wt'] == '':
        declar_horse_wt = 0
    elif '-' in row['declar_horse_wt']:
        declar_horse_wt = -999
    else:
        declar_horse_wt = int(row['declar_horse_wt'])

    if '-' in row['draw']:
        draw = 0
    else:
        draw = int(row['draw'])

    season_stakes = horse_info['season_stakes']
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

    item = (race_date, race_id, horse_no, pla_odds, win_odds, plc, count, race_no, site, cls, distance, bonus, going,
            course, actual_wt, declar_horse_wt, draw, current_rating, season_stakes, total_stakes, horse_age,
            horse_star_0_curRace, horse_star_1_curRace, horse_star_2_curRace, horse_star_3_curRace, horse_total_curRace,
            horse_star_0_allRace, horse_star_1_allRace, horse_star_2_allRace, horse_star_3_allRace, horse_total_allRace,
            horse_deltaDays, horse_score, horse_speed[0], horse_speed[1], dis_ave_speed, go_ave_speed, new_dis_array[0],
            new_dis_array[1], new_dis_array[2], new_dis_array[3])
    return item


def main():
    results_list = __searchAllResultsData()
    horse_dict = __searchAllHorse()
    if len(results_list) > 0:
        data_dict = source_datas.prepareDatas(results_list)
        all_list = []
        for row in results_list:
            # horse info
            horse_info = source_datas.getHorseInfo(row, horse_dict)
            # race count
            race_count = source_datas.getRaceCount(row, data_dict['race_count'])
            # horse starts
            horse_starts = source_datas.getHorseStartsInfo(row, data_dict['horse_raceStarts'], data_dict['horse_allRaceStarts'])
            # horse deltaDays
            horse_deltaDays = source_datas.getHorseDeltaDays(row, data_dict['horse_deltaDays'])
            # horse score
            horse_score = source_datas.getHorseScore(row, data_dict['horse_score'])
            # horse age
            horse_age = source_datas.getHorseAge(row, data_dict['horse_age'])
            # horse speed
            horse_speed = source_datas.getHorseSpeed(row, data_dict['horse_speed'])
            # current rating before
            current_rating = source_datas.getCurrentRating(row, data_dict['current_rating'])
            # dis_ave_speed
            dis_ave_speed = source_datas.getDistanceAveSpeed(row, data_dict['dis_avesr'])
            # dis_ave_speed
            go_ave_speed = source_datas.getGoingAveSpeed(row, data_dict['go_aversr'])
            # new_dis, rest, act_delta, dct_delta
            new_dis_array = source_datas.getNewDis(row, data_dict['horse_newDis'])

            # 将数据组装成目标数据结构
            cur_row = __toTargetStruct(row, race_count, horse_info, horse_age, horse_starts,
                                       horse_score, horse_speed, current_rating, horse_deltaDays, dis_ave_speed,
                                       go_ave_speed, new_dis_array)
            item = (cur_row)
            all_list.append(item)

        export.export(all_list)
    else:
        pass



