from db.db import singleton_ResultsDB

# TODAY_TABLE = 'today_table_dragon_{0}'
TODAY_TABLE = 'today_table_dragon_model2_5_{0}'


def getTodayTable(race_date):
    today_dict = {}  # race_no & {horse_no & row}
    update_table = TODAY_TABLE.replace('{0}', race_date)
    if singleton_ResultsDB.table_exists(update_table):
        singleton_ResultsDB.cursor.execute('select * from {}'.format(update_table))
        rows = singleton_ResultsDB.cursor.fetchall()
        singleton_ResultsDB.connect.commit()
        for row in rows:
            race_no = row['race_no']
            horse_no = row['horse_no']
            if race_no not in today_dict.keys():
                today_dict[race_no] = {}
            today_dict[race_no][horse_no] = row
    else:
        print('today table[', update_table, '] not exist')

    count = 0
    for race_no, dict in today_dict.items():
        count += len(dict)
    print(race_date, 'today count=', count)

    return today_dict

