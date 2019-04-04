from check_today_table import lastest_data


def __getLastestOdds(lastest_dict):
    odds_dict = {}  # race_no & {horse_no & [win_odds, pla_odds]}
    for race_no, dict in lastest_dict.items():
        if race_no not in odds_dict.keys():
            odds_dict[race_no] = {}
        for horse_no, row in dict.items():
            if row['exit_race'] == 1:
                continue
            odds_dict[race_no][horse_no] = [float(row['win_odds']), float(row['pla_odds'])]
    return odds_dict


# lastest_dict: race_no & {horse_no & row}
def main():
    race_date = '20190306'
    lastest_dict = lastest_data.getLastestRows(race_date)
    odds_dict = __getLastestOdds(lastest_dict)
    for race_no, dict in odds_dict.items():
        print(race_no, dict)


if __name__ == '__main__':
    main()

