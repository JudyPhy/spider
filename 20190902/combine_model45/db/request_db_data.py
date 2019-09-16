from db.database import singleton_Results_DB
from db.database import singleton_Scrub_DB
from common import common


def __requestModelRows(tableName):
    model_rows = {}   # race_date_No & {horse_No & row}
    if singleton_Results_DB.table_exists(tableName):
        singleton_Results_DB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in rows:
            cur_race_date = row['race_date']
            race_No = row['race_no']
            race_date_No = str(cur_race_date) + common.toDoubleDigitStr(race_No)
            if race_date_No not in model_rows.keys():
                model_rows[race_date_No] = {}
            horse_No = row['horse_no']
            model_rows[race_date_No][horse_No] = row
    return model_rows


def RequestModel4Rows():
    return __requestModelRows(common.HISTORY_MODEL4_TABLE)


def RequestModel5Rows():
    return __requestModelRows(common.HISTORY_MODEL5_TABLE)


def RequestSectionalOddsRows():
    odds_sectional_rows = {}    # race_date_No & {horse_No & row}
    tableName = common.ODDS_SECTIONAL_TABLE
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            race_date = row['race_date']
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            if race_date_No not in odds_sectional_rows.keys():
                odds_sectional_rows[race_date_No] = {}
            horse_No = row['horse_No']
            odds_sectional_rows[race_date_No][horse_No] = row
    return odds_sectional_rows


def RequestImmdSectionalOdds():
    odds_immd_sectional_rows = {}    # race_date_No & {horse_No & row}
    tableName = common.ODDS_IMMD_SECTIONAL_TABLE
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            race_date = row['race_date']
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            if race_date_No not in odds_immd_sectional_rows.keys():
                odds_immd_sectional_rows[race_date_No] = {}
            horse_No = row['horse_No']
            odds_immd_sectional_rows[race_date_No][horse_No] = row
    return odds_immd_sectional_rows

