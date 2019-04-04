from check_today_table import today_table


def main():
    race_date = '20190306'
    today_table_dict = today_table.getTodayTable(race_date)
    for race_no, dict in today_table_dict.items():
        print(race_no, len(dict))


if __name__ == '__main__':
    main()

