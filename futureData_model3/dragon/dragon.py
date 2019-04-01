### 根据合并表的数据，制作新结构的数据表 ###
from db.database import singleton_Scrub_DB
from common import common
from dragon import source_datas
from dragon import export
import datetime
from config.myconfig import singleton_cfg


def __searchAllRaceCardData(today_date):
    all = []
    # history
    now = datetime.datetime.now()
    for year in range(2014, now.year + 1):
        tableName = common.RECE_CARD_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                if int(row['race_date']) < int(today_date):
                    draw = row['draw'].replace('\xa0', '')
                    if '' != draw:
                        all.append(row)
        else:
            common.log('dragon: Table[' + tableName + '] not exist.')
    count = len(all)
    print('without future raceCard=', count)

    # today
    future_table = common.FUTURE_RECE_CARD_TABLE.replace('{0}', today_date[: len(today_date) - 4])
    if singleton_Scrub_DB.table_exists(future_table):
        singleton_Scrub_DB.cursor.execute('select * from {} where race_date=%s'.format(future_table), today_date)
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            draw = row['draw'].replace('\xa0', '')
            if '' != draw:
                all.append(row)
            else:
                print('future draw error:', row)
    else:
        common.log('dragon: Table[' + future_table + '] not exist.')
    print('all raceCard=', len(all), ' future=', len(all) - count)
    return all


def __getAllResultsRows(today_date):
    all = {}    # race_date_No & {horse_code & row}
    now = datetime.datetime.now()
    for year in range(2014, now.year + 1):
        tableName = common.RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                array_date = row['race_date'].split('/')
                race_date = array_date[2] + array_date[1] + array_date[0]
                if int(race_date) < int(today_date):
                    race_date_No = race_date + common.toDoubleDigitStr(row['race_No'])
                    if race_date_No not in all.keys():
                        all[race_date_No] = {}
                    horse_code = row['horse_code'].strip()
                    if horse_code not in all[race_date_No].keys():
                        all[race_date_No][horse_code] = row
        else:
            common.log('results: Table[' + tableName + '] not exist.')
    count = 0
    for race_date_No, dict in all.items():
        count += len(dict)
    print('all results=', count)
    return all


# 将原数据转成目标数据结构
def __toTargetStruct(row, last_race_id, pedigree_dst_dict,
                     horse_record_dict, horse_recent_record_dict, horse_site_record_dict, horse_go_record_dict,
                     horse_course_record_dict, horse_dst_record_dict, horse_cls_record_dict, horse_draw_record_dict,
                     horse_jockey_record_dict, horse_speed_dict, horse_recent_speed_dict, horse_site_speed_dict,
                     horse_go_speed_dict, horse_course_speed_dict, horse_dst_speed_dict, horse_cls_speed_dict,
                     horse_draw_speed_dict, horse_gear_speed_dict, horse_jockey_speed_dict,
                     rtg_dict, horse_dct_trend_dict, horse_act_trend_dict,
                     horse_rest_dict, horse_new_dis_dict, draw_record_dict, trainer_record_dict,
                     jockey_record_dict, jockey_recent_dict, jockey_hot_dict, jockey_hot_before4_dict):
    race_date = row['race_date']    # 20190202 str
    race_no = row['race_No']
    __race_date_No = race_date + common.toDoubleDigitStr(race_no)
    horse_no = row['horse_No']
    horse_code = row['horse_code'].strip()
    race_id = race_no
    pla_odds = 1
    win_odds = 1
    plc = 999

    array_trainer = row['trainer'].split('(')
    trainer_code = array_trainer[0].strip()

    array_jockey = row['jockey'].split('(')
    jockey_code = array_jockey[0].strip()

    site_label = row['site'].replace(' ', '')

    go_label = row['going'].replace(' ', '').upper()
    if go_label == '':
        go_label = 'GOOD'

    course_label = row['course'].strip()
    dst_label = int(row['distance'])
    cls_label = row['cls'].strip()
    draw_label = int(row['draw'])
    gear_label = row['gear']
    count_bucket = ''
    odd_bucket = ''
    pedigree_growth = False
    pedigree_dst = source_datas.getPedigreeDst(__race_date_No, horse_code, pedigree_dst_dict)
    pedigree_track = False
    horse_age = int(row['age'])

    horse_record = source_datas.getHorseRecord(__race_date_No, horse_code, horse_record_dict)
    horse_recent_record = source_datas.getHorseRecentRecord(__race_date_No, horse_code, horse_recent_record_dict)
    horse_site_record = source_datas.getHorseSiteRecord(__race_date_No, horse_code, horse_site_record_dict)
    horse_go_record = source_datas.getHorseGoingRecord(__race_date_No, horse_code, horse_go_record_dict)
    horse_course_record = source_datas.getHorseCourseRecord(__race_date_No, horse_code, horse_course_record_dict)
    horse_dst_record = source_datas.getHorseDstRecord(__race_date_No, horse_code, horse_dst_record_dict)
    horse_cls_record = source_datas.getHorseClsRecord(__race_date_No, horse_code, horse_cls_record_dict)
    horse_draw_record = source_datas.getHorseDrawRecord(__race_date_No, horse_code, horse_draw_record_dict)
    # horse_count_record
    horse_jockey_record = source_datas.getHorseJockeyRecord(__race_date_No, horse_code, horse_jockey_record_dict)
    # horse_odd_record

    horse_speed = source_datas.getHorseSpeed(__race_date_No, horse_code, horse_speed_dict)
    horse_recent_speed = source_datas.getHorseRecentSpeed(__race_date_No, horse_code, horse_recent_speed_dict)
    horse_site_speed = source_datas.getHorseSiteSpeed(__race_date_No, horse_code, horse_site_speed_dict)
    horse_go_speed = source_datas.getHorseGoSpeed(__race_date_No, horse_code, horse_go_speed_dict)
    horse_course_speed = source_datas.getHorseCourseSpeed(__race_date_No, horse_code, horse_course_speed_dict)
    horse_dst_speed = source_datas.getHorseDstSpeed(__race_date_No, horse_code, horse_dst_speed_dict)
    horse_cls_speed = source_datas.getHorseClsSpeed(__race_date_No, horse_code, horse_cls_speed_dict)
    horse_draw_speed = source_datas.getHorseClsSpeed(__race_date_No, horse_code, horse_draw_speed_dict)
    horse_gear_speed = source_datas.getHorseGearSpeed(__race_date_No, horse_code, horse_gear_speed_dict)
    # horse_count_speed
    horse_jockey_speed = source_datas.getHorseJockeySpeed(__race_date_No, horse_code, horse_jockey_speed_dict)
    # horse_odd_speed
    horse_last_dst_time = -1

    current_rating = source_datas.getRtg(__race_date_No, horse_code, rtg_dict)

    declar_horse_wt = row['horse_wt_dec']
    if ('\xa0' in declar_horse_wt) and (plc == None):
        declar_horse_wt = 0
    else:
        declar_horse_wt = int(declar_horse_wt)

    actual_wt = int(row['wt'])

    rating_trend = row['rtg_as']
    if '-' == rating_trend:
        rating_trend = 0
    else:
        rating_trend = int(rating_trend)

    dct_trend = source_datas.getHorseDctTrend(__race_date_No, horse_code, horse_dct_trend_dict)
    act_trend = source_datas.getHorseActTrend(__race_date_No, horse_code, horse_act_trend_dict)
    odd_trend = 0
    odd_sectional_trend = 1

    rest = source_datas.getHorseRest(__race_date_No, horse_code, horse_rest_dict)
    # age_match
    # dst_match
    # track_match
    new_dis = source_datas.getHorseNewDis(__race_date_No, horse_code, horse_new_dis_dict)

    draw_record = source_datas.getDrawRecord(race_date, draw_label, draw_record_dict)
    trainer_record = source_datas.getTrainerRecord(race_date, trainer_code, trainer_record_dict)
    jockey_record = source_datas.getJockeyRecord(race_date, jockey_code, jockey_record_dict)
    jockey_recent = source_datas.getJockeyRecent(race_date, jockey_code, jockey_recent_dict)

    jockey_hot = source_datas.getJockeyHot(__race_date_No, horse_code, jockey_hot_dict)
    jockey_hot_before4 = source_datas.getJockeyHotBefore4(__race_date_No, horse_code, jockey_hot_before4_dict)

    item = (race_date, race_id, race_no, horse_no, pla_odds, win_odds, plc, horse_code, trainer_code, jockey_code,
            site_label, go_label, course_label, dst_label, cls_label, draw_label, gear_label, count_bucket, odd_bucket, pedigree_growth,
            pedigree_dst, pedigree_track, horse_age,
            horse_record[0] + horse_record[1] + horse_record[2] + horse_record[3], horse_record[4],
            horse_recent_record[0] + horse_recent_record[1] + horse_recent_record[2] + horse_recent_record[3], horse_recent_record[4],
            horse_site_record[0] + horse_site_record[1] + horse_site_record[2] + horse_site_record[3], horse_site_record[4],
            horse_go_record[0] + horse_go_record[1] + horse_go_record[2] + horse_go_record[3], horse_go_record[4],
            horse_course_record[0] + horse_course_record[1] + horse_course_record[2] + horse_course_record[3], horse_course_record[4],
            horse_dst_record[0] + horse_dst_record[1] + horse_dst_record[2] + horse_dst_record[3], horse_dst_record[4],
            horse_cls_record[0] + horse_cls_record[1] + horse_cls_record[2] + horse_cls_record[3], horse_cls_record[4],
            horse_draw_record[0] + horse_draw_record[1] + horse_draw_record[2] + horse_draw_record[3], horse_draw_record[4],
            horse_jockey_record[0] + horse_jockey_record[1] + horse_jockey_record[2] + horse_jockey_record[3], horse_jockey_record[4],
            horse_speed[0], horse_speed[1], horse_speed[2],
            horse_recent_speed[0], horse_recent_speed[1], horse_recent_speed[2],
            horse_site_speed[0], horse_site_speed[1], horse_site_speed[2],
            horse_go_speed[0], horse_go_speed[1], horse_go_speed[2],
            horse_course_speed[0], horse_course_speed[1], horse_course_speed[2],
            horse_dst_speed[0], horse_dst_speed[1], horse_dst_speed[2],
            horse_cls_speed[0], horse_cls_speed[1], horse_cls_speed[2],
            horse_draw_speed[0], horse_draw_speed[1], horse_draw_speed[2],
            horse_gear_speed[0], horse_gear_speed[1], horse_gear_speed[2],
            horse_jockey_speed[0], horse_jockey_speed[1], horse_jockey_speed[2],
            current_rating, declar_horse_wt, actual_wt, rating_trend, dct_trend, act_trend, odd_trend, rest, new_dis,
            draw_record[0] + draw_record[1] + draw_record[2] + draw_record[3], draw_record[4],
            trainer_record[0] + trainer_record[1] + trainer_record[2] + trainer_record[3], trainer_record[4],
            jockey_record[0] + jockey_record[1] + jockey_record[2] + jockey_record[3], jockey_record[4],
            jockey_recent[0] + jockey_recent[1] + jockey_recent[2] + jockey_recent[3], jockey_recent[4],
            horse_last_dst_time, jockey_hot, jockey_hot_before4, odd_sectional_trend)
    return item


def main():
    today_date = singleton_cfg.getRaceDate()
    raceCard_rows = __searchAllRaceCardData(today_date)
    results_rows = __getAllResultsRows(today_date)    # race_date_No & {horse_code & row}
    if len(raceCard_rows) > 0:
        data_dict = source_datas.prepareDatas(raceCard_rows, results_rows)
        last_race_id = source_datas.getLastRaceId(today_date, results_rows)  # race_date: '20190101'
        all_list = []
        print('start data=>')
        for row in raceCard_rows:
            race_date = row['race_date']
            if today_date == race_date:
                # pedigree_dst
                pedigree_dst_dict = data_dict['pedigree_dst']
                # horse_record
                horse_record_dict = data_dict['horse_record']
                # horse_recent_record
                horse_recent_record_dict = data_dict['horse_recent_record']
                # horse_site_record
                horse_site_record_dict = data_dict['horse_site_record']
                # horse_go_record
                horse_go_record_dict = data_dict['horse_go_record']
                # horse_course_record
                horse_course_record_dict = data_dict['horse_course_record']
                # horse_dst_record
                horse_dst_record_dict = data_dict['horse_dst_record']
                # horse_cls_record
                horse_cls_record_dict = data_dict['horse_cls_record']
                # horse_draw_record
                horse_draw_record_dict = data_dict['horse_draw_record']
                # horse_jockey_record
                horse_jockey_record_dict = data_dict['horse_jockey_record']
                # horse_speed
                horse_speed_dict = data_dict['horse_speed']
                # horse_recent_speed
                horse_recent_speed_dict = data_dict['horse_recent_speed']
                # horse_site_speed
                horse_site_speed_dict = data_dict['horse_site_speed']
                # horse_go_speed
                horse_go_speed_dict = data_dict['horse_go_speed']
                # horse_course_speed
                horse_course_speed_dict = data_dict['horse_course_speed']
                # horse_dst_speed
                horse_dst_speed_dict = data_dict['horse_dst_speed']
                # horse_cls_speed
                horse_cls_speed_dict = data_dict['horse_cls_speed']
                # horse_draw_speed
                horse_draw_speed_dict = data_dict['horse_draw_speed']
                # horse_gear_speed
                horse_gear_speed_dict = data_dict['horse_gear_speed']
                # horse_jockey_speed
                horse_jockey_speed_dict = data_dict['horse_jockey_speed']
                # rtg
                rtg_dict = data_dict['rtg']
                # horse_dct_trend
                horse_dct_trend_dict = data_dict['horse_dct_trend']
                # horse_act_trend
                horse_act_trend_dict = data_dict['horse_act_trend']
                # horse_rest
                horse_rest_dict = data_dict['horse_rest']
                # horse_new_dis
                horse_new_dis_dict = data_dict['horse_new_dis']
                # draw_record
                draw_record_dict = data_dict['draw_record']
                # trainer_record
                trainer_record_dict = data_dict['trainer_record']
                # jockey_record
                jockey_record_dict = data_dict['jockey_record']
                # jockey_recent
                jockey_recent_dict = data_dict['jockey_recent']
                # jockey_hot
                jockey_hot_dict = data_dict['jockey_hot']
                # jockey_hot_before4
                jockey_hot_before4_dict = data_dict['jockey_hot_before4']

                # 将数据组装成目标数据结构
                cur_row = __toTargetStruct(row, last_race_id, pedigree_dst_dict,
                                           horse_record_dict, horse_recent_record_dict, horse_site_record_dict, horse_go_record_dict,
                                           horse_course_record_dict, horse_dst_record_dict, horse_cls_record_dict, horse_draw_record_dict,
                                           horse_jockey_record_dict, horse_speed_dict, horse_recent_speed_dict, horse_site_speed_dict,
                                           horse_go_speed_dict, horse_course_speed_dict, horse_dst_speed_dict, horse_cls_speed_dict,
                                           horse_draw_speed_dict, horse_gear_speed_dict, horse_jockey_speed_dict,
                                           rtg_dict, horse_dct_trend_dict, horse_act_trend_dict,
                                           horse_rest_dict, horse_new_dis_dict, draw_record_dict, trainer_record_dict,
                                           jockey_record_dict, jockey_recent_dict, jockey_hot_dict, jockey_hot_before4_dict)
                item = (cur_row)
                all_list.append(item)

        export.export(all_list)

        source_datas.showLostPedigreeDst()
    else:
        pass



