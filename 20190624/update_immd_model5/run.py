from update_model5 import update_race_info as update_data_model5
from db import request_db_data
from config.myconfig import singleton_cfg


def main():
    race_date = singleton_cfg.getRaceDate()
    race_results_rows = request_db_data.RequestRaceResultsRows(race_date)   # race_date_No & {horse_code & row}
    race_card_history_rows = request_db_data.RequestRaceCardHistoryRows(race_date)  # race_date_No & {horse_code & row}
    # display_sectional_time_rows = request_db_data.RequestDisplaySectionalTimeRows(race_date)    # race_date_No & {horse_code & row}
    today_race_start_time = request_db_data.RequestTodayRaceStartTime(race_date)   # race_No & [start_time, before10_time]
    while(True):
        today_table_rows = request_db_data.RequestTodayTableRows()  # update_table & {race_No & {horse_No & row}}
        immd_rows = request_db_data.RequestImmdRows(race_date)    # race_No & {horse_No & row}
        lastest_rows = request_db_data.RequestLastestRows(race_date)    # race_No & {horse_No & row}

        for update_table, dict in today_table_rows.items():
            if 'model5' in update_table:
                update_data_model5.updateModel5(update_table, dict, immd_rows, lastest_rows, race_results_rows,
                                                race_card_history_rows, today_race_start_time)


if __name__ == '__main__':
    main()



