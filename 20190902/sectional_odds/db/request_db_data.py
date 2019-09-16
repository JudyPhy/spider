from db.database import singleton_Scrub_DB
from common import common


def RequestImmdOddsRows():
    immd_odds_rows = {}   # race_date_No & {horse_No & rows}
    tableName = common.ODDS_IMMD_TABLE
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            cur_race_date = row['race_date']
            race_No = row['race_No']
            race_date_No = cur_race_date + common.toDoubleDigitStr(race_No)
            if race_date_No not in immd_odds_rows.keys():
                immd_odds_rows[race_date_No] = {}
            horse_No = row['horse_No']
            if horse_No not in immd_odds_rows[race_date_No].keys():
                immd_odds_rows[race_date_No][horse_No] = []
            immd_odds_rows[race_date_No][horse_No].append(row)
    return immd_odds_rows

