from update_odds import update_odds
from update_odds import update_odds_sectional_trend
from update_count import update_count
from check_horse import check_horse
from update_going import update_going
from update_wt import update_wt
import lastest_data
import today_table


def main():
    today_race_time = today_table.getTodayRaceStartTime()   # race_No & [start_time, before10_time]
    while(True):
        today_table_dict = today_table.getTodayTable()  # update_table & {race_no & {horse_no & row}}
        lastest_dict = lastest_data.getLastestRows()    # race_no & {horse_no & row} 退赛马匹赔率不会被爬取到赔率变化表
        # update odds
        update_odds.updateOdds(today_table_dict, lastest_dict)

        # update odds sectional trend
        update_odds_sectional_trend.updateOddsSectionalTrend(today_table_dict, today_race_time)

        # check horse code
        check_horse.checkHorse(today_table_dict, lastest_dict)

        # check count and update
        update_count.updateExitRace(today_table_dict, lastest_dict)

        # update going
        update_going.updateGoing(today_table_dict, lastest_dict)

        # update wt
        update_wt.updateWt(today_table_dict, lastest_dict)


if __name__ == '__main__':
    main()



