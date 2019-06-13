from common import common
import datetime
from db.database import singleton_Scrub_DB


def __getAllSectionalOdds():
    odds_sectional_dict = {}    # race_date_No & {horse_No & row}
    for year in range(2014, datetime.datetime.now().year + 1):
        tableName = common.ODDS_SECTIONAL_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                race_date = row['race_date']
                race_No = row['race_No']
                race_date_No = race_date + common.toDoubleDigitStr(race_No)
                if race_date_No not in odds_sectional_dict.keys():
                    odds_sectional_dict[race_date_No] = {}
                horse_No = row['horse_No']
                odds_sectional_dict[race_date_No][horse_No] = row
        else:
            print('dragon: Table[' + tableName + '] not exist.')
    return odds_sectional_dict


def getOddsSectionalTrend(raceCard_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    no_sectional_odds = []
    odds_sectional_dict = __getAllSectionalOdds()   # race_date_No & {horse_No & row}
    odds_sectional_trend_dict = {}  # race_date_No & {horse_code & odds_sectional_trend}
    for race_date_No, rows in temp_raceCard_rows.items():
        if race_date_No not in odds_sectional_trend_dict.keys():
            odds_sectional_trend_dict[race_date_No] = {}
        for row in rows:
            horse_code = row['horse_code'].strip()
            horse_No = row['horse_No']
            if (race_date_No in odds_sectional_dict.keys()) and (horse_No in odds_sectional_dict[race_date_No]):
                odds3 = odds_sectional_dict[race_date_No][horse_No]['odds3']
                odds4 = odds_sectional_dict[race_date_No][horse_No]['odds4']
                if odds3 == '' or odds4 == '':
                    # print(race_date_No, 'odds none:', odds3, odds4)
                    odds_sectional_trend_dict[race_date_No][horse_code] = 1
                else:
                    odds_sectional_trend_dict[race_date_No][horse_code] = float(odds4)/float(odds3)
            else:
                no_sectional_odds.append([race_date_No, horse_No])
                odds_sectional_trend_dict[race_date_No][horse_code] = 1
    return odds_sectional_trend_dict


