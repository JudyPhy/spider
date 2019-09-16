from common import common
from pedigree_dst import pedigree_dst
from results_table import results_table
from horse_record import horse_record
from horse_record import horse_recent_record
from horse_record import horse_site_record
from horse_record import horse_go_record
from horse_record import horse_course_record
from horse_record import horse_dst_record
from horse_record import horse_cls_record
from horse_record import horse_draw_record
from horse_record import horse_jockey_record
from horse_speed import horse_speed
from horse_speed import horse_recent_speed
from horse_speed import horse_site_speed
from horse_speed import horse_go_speed
from horse_speed import horse_course_speed
from horse_speed import horse_dst_speed
from horse_speed import horse_cls_speed
from horse_speed import horse_draw_speed
from horse_speed import horse_jockey_speed
from horse_speed import horse_gear_speed
from horse_speed import horse_last_dst_time
from horse_trend import horse_dct_trend
from horse_trend import horse_act_trend
from horse_trend import horse_odds_trend
from horse_trend import horse_odds_sectional_trend
from horse_rest import horse_rest
from horse_new_dis import horse_new_dis
from record import draw_record
from record import trainer_record
from record import jockey_record
from record import jockey_recent
from record import jockey_trainer_record
from hot import jockey_hot


def getRaceId(race_date_No, horse_code, sort_history_raceResults_rows):
    if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
        year = int(race_date_No[len(race_date_No) - 8: len(race_date_No) - 6])
        month = int(race_date_No[len(race_date_No) - 6: len(race_date_No) - 4])
        if month < 8:
            year -= 1
        race_id = sort_history_raceResults_rows[race_date_No][horse_code]['race_id']
        new_race_id = int(str(year) + common.toThreeDigitStr(race_id))
        return new_race_id
    print("RaceId can't find:", race_date_No, horse_code)
    return -1


def getValue(race_date_No, horse_code, dict, defalut_value):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("Value can't find:", race_date_No, horse_code)
    return defalut_value


def getRecords(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        records = dict[race_date_No][horse_code]
        return [records[0] + records[1] + records[2] + records[3], records[4]]
    print(race_date_No, horse_code, " can't find records")
    return [0, 0]


def getSpeeds(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print(race_date_No, horse_code, " can't find speeds")
    return [0, 0, 0]


def getHorseOddsSectionalTrend(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    # print("HorseOddsSectionalTrend can't find:", race_date_No, horse_code)
    return 1


def __toRaceDateRows(sort_history_raceCard_rows):
    sort_race_date_rows = {} # race_date & [rows]
    for race_date_No, dict in sort_history_raceCard_rows.items():
        race_date = race_date_No[: len(race_date_No) - 2]
        if race_date not in sort_race_date_rows.keys():
            sort_race_date_rows[race_date] = []
        for horse_code, row in dict.items():
            sort_race_date_rows[race_date].append(row)
    return sort_race_date_rows


def prepareDatas(sort_history_raceCard_rows, sort_history_raceResults_rows, horse_pedigree_rows, display_sectional_time_rows, odds_sectional_rows, odds_immd_sectional_rows):
    data_dict = {}
    data_dict['race_info'] = results_table.GetRaceInfoDict(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['pedigree_dst'] = pedigree_dst.GetPedigreeDistanceDict(sort_history_raceCard_rows, horse_pedigree_rows)

    data_dict['horse_record'] = horse_record.GetHorseRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_recent_record'] = horse_recent_record.GetHorseRecentRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_site_record'] = horse_site_record.GetHorseSiteRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_going_record'] = horse_go_record.GetHorseGoingRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_course_record'] = horse_course_record.GetHorseCourseRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_dst_record'] = horse_dst_record.GetHorseDstRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_cls_record'] = horse_cls_record.GetHorseClsRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_draw_record'] = horse_draw_record.GetHorseDrawRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_jockey_record'] = horse_jockey_record.GetHorseJockeyRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)

    data_dict['horse_speed'] = horse_speed.GetHorseSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_recent_speed'] = horse_recent_speed.GetHorseRecentSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_site_speed'] = horse_site_speed.GetHorseSiteSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_going_speed'] = horse_go_speed.GetHorseGoSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_course_speed'] = horse_course_speed.GetHorseCourseSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_dst_speed'] = horse_dst_speed.GetHorseDstSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_cls_speed'] = horse_cls_speed.GetHorseClsSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_draw_speed'] = horse_draw_speed.GetHorseDrawSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_gear_speed'] = horse_gear_speed.GetHorseGearSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_jockey_speed'] = horse_jockey_speed.GetHorseJockeySpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_last_dst_time'] = horse_last_dst_time.GetHorseLastDstTimePrev(sort_history_raceCard_rows, sort_history_raceResults_rows, display_sectional_time_rows)

    data_dict['horse_dct_trend'] = horse_dct_trend.GetHorseDctTrend(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_act_trend'] = horse_act_trend.GetHorseActTrend(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_odds_trend'] = horse_odds_trend.GetHorseWinOddsTrend(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_odds_sectional_trend'] = horse_odds_sectional_trend.getOddsSectionalTrend(sort_history_raceCard_rows, sort_history_raceResults_rows, odds_sectional_rows, odds_immd_sectional_rows)

    data_dict['horse_rest'] = horse_rest.GetHorseRest(sort_history_raceCard_rows, sort_history_raceResults_rows)

    data_dict['horse_new_dis'] = horse_new_dis.GetHorseNewDis(sort_history_raceCard_rows, sort_history_raceResults_rows)

    sort_race_date_rows = __toRaceDateRows(sort_history_raceCard_rows)
    data_dict['draw_record'] = draw_record.GetDrawRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['trainer_record'] = trainer_record.GetTrainerRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['jockey_record'] = jockey_record.GetJockeyRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['jockey_recent'] = jockey_recent.GetJockeyRecent(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['jockey_trainer_record'] = jockey_trainer_record.GetJockeyTrainerRecord(sort_race_date_rows, sort_history_raceResults_rows)

    data_dict['jockey_hot'] = jockey_hot.GetJockeyHot(sort_history_raceCard_rows, sort_history_raceResults_rows)

    # for race_date_No, dict in data_dict['jockey_hot'].items():
    #     print(race_date_No, dict)

    return data_dict

