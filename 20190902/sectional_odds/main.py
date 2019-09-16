# coding=gbk
from db import request_db_data
import to_sectional_odds
from db import exportToDb


def main():
    orig_immd_odds_rows = request_db_data.RequestImmdOddsRows()  # race_date_No & {horse_No & rows}
    sectional_odds_rows = to_sectional_odds.GetSectionalOddsRows(orig_immd_odds_rows)
    all_list = []
    for race_date_No, rows_dict in sectional_odds_rows.items():
        # print(race_date_No, rows_dict)
        for horse_No, odds_array in rows_dict.items():
            race_date = race_date_No[: len(race_date_No) - 2]
            race_No = int(race_date_No[len(race_date_No) - 2:])
            cur_line = [race_date, race_No, horse_No, odds_array[3], odds_array[2], odds_array[1], odds_array[0]]
            cur_line = (cur_line)
            all_list.append(cur_line)
    exportToDb.exportToSectionalOddsTable(all_list)


main()
