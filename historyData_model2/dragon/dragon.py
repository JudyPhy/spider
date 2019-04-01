### 根据合并表的数据，制作新结构的数据表 ###
from db.database import singleton_Scrub_DB
from common import common
from dragon import source_datas
from dragon import export
import datetime

RESULTS_TABLE = 'f_race_results_{0}'


def __searchAllResultsData():
    results = []
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
            rows = singleton_Scrub_DB.cursor.fetchall()
            for row in rows:
                array = row['race_date'].split('/')
                row['race_date'] = int(array[2] + array[1] + array[0])  # 20190202 int
                results.append(row)
            singleton_Scrub_DB.connect.commit()
        else:
            common.log('dragon: Table[' + tableName + '] not exist.')
    return results


def toSeasonID(race_date):
    str_raceDate = str(race_date)
    str_year = str_raceDate[:len(str_raceDate) - 4]
    year = int(str_year[len(str_year) - 2:])
    month = int(str_raceDate[len(str_raceDate) - 4:len(str_raceDate) - 2])
    if month < 8:
        return year - 1
    else:
        return year


# 将原数据转成目标数据结构
def __toTargetStruct(row, race_count, season_stakes, total_stakes, horse_age, horse_starts, horse_score, horse_speed, current_rating, rtg,
                     horse_deltaDays, dis_ave_speed, dis_ave_horse_speed, go_ave_speed, go_ave_horse_speed, new_dis_array,
                     jockey_trainer_count, horse_jockey_count, horse_trainer_count):
    race_date = row['race_date']
    seasonId = toSeasonID(row['race_date'])
    # print('race_date:', row['race_date'], ' seasonId:', seasonId)
    race_id = int(str(seasonId) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
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

    item = (race_date, race_id, horse_code, horse_no, pla_odds, win_odds, plc, race_count, race_no, site, cls, distance, bonus, going,
            course, actual_wt, declar_horse_wt, draw, rtg, season_stakes, total_stakes, horse_age,
            horse_star_0_curRace, horse_star_1_curRace, horse_star_2_curRace, horse_star_3_curRace, horse_total_curRace,
            horse_star_0_allRace, horse_star_1_allRace, horse_star_2_allRace, horse_star_3_allRace, horse_total_allRace,
            horse_deltaDays, horse_score, horse_speed[0], horse_speed[1], dis_ave_speed, dis_ave_horse_speed,
            go_ave_speed, go_ave_horse_speed, new_dis_array[0], new_dis_array[1], new_dis_array[2], new_dis_array[3],
            jockey_trainer_count[0], jockey_trainer_count[1], horse_jockey_count[0], horse_jockey_count[1],
            horse_trainer_count[0], horse_trainer_count[1])
    return item


def main():
    results_list = __searchAllResultsData()
    print('all results count=', len(results_list))
    if len(results_list) > 0:
        data_dict = source_datas.prepareDatas(results_list)
        all_list = []
        for row in results_list:
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
            rtg = source_datas.getRtg(row, data_dict['rtg'])
            # dis_ave_speed
            dis_ave_speed = source_datas.getDistanceAveSpeed(row, data_dict['dis_avesr'])
            # dis_ave_horse_speed
            dis_ave_horse_speed = source_datas.getDistanceAveHorseSpeed(row, data_dict['dis_avesr_horse'])
            # go_ave_speed
            go_ave_speed = source_datas.getGoingAveSpeed(row, data_dict['go_aversr'])
            # go_ave_horse_speed
            go_ave_horse_speed = source_datas.getGoingAveHorseSpeed(row, data_dict['go_aversr_horse'])
            # new_dis, rest, act_delta, dct_delta
            new_dis_array = source_datas.getNewDis(row, data_dict['horse_newDis'])
            # season_stakes
            season_stakes = source_datas.getSeasonStakes(row, data_dict['season_stakes'])
            # total_stakes
            total_stakes = source_datas.getTotalStakes(row, data_dict['total_stakes'])
            # jockey_trainer_count
            jockey_trainer_count = source_datas.getHorseJockeyTrainerRaceCount(row, data_dict['jt_raceCount'])
            # horse_jockey_count
            horse_jockey_count = source_datas.getHorseJockeyTrainerRaceCount(row, data_dict['hj_raceCount'])
            # horse_trainer_count
            horse_trainer_count = source_datas.getHorseJockeyTrainerRaceCount(row, data_dict['ht_raceCount'])

            # 将数据组装成目标数据结构
            cur_row = __toTargetStruct(row, race_count, season_stakes, total_stakes, horse_age, horse_starts,
                                       horse_score, horse_speed, current_rating, rtg, horse_deltaDays, dis_ave_speed, dis_ave_horse_speed,
                                       go_ave_speed, go_ave_horse_speed, new_dis_array, jockey_trainer_count, horse_jockey_count,
                                       horse_trainer_count)
            item = (cur_row)
            all_list.append(item)

        export.export(all_list)
    else:
        pass



