from db.db import singleton_ScrubDb
from common import common
from url.race_dividend_url import RaceDividendUrl


def __getRaceId(race_date, race_No, race_date_No_id_dict):
    if (race_date in race_date_No_id_dict.keys()) and (race_No in race_date_No_id_dict[race_date].keys()):
        return int(race_date_No_id_dict[race_date][race_No])
    # if race_date == '20161026' and race_No == 4:
    #     return 134
    print('error race_id:', race_date, race_No)
    return 0


def exportToDb(race_date, dividend_dict, race_date_No_id_dict):
    if len(dividend_dict) <= 0:
        return
    tableName = RaceDividendUrl().EXPORT_TABLE
    __createTable(tableName)
    for race_No, rows in dividend_dict.items():
        try:
            singleton_ScrubDb.cursor.execute("select * from {} where race_date=%s and race_No=%s".format(tableName),
                                             (race_date, race_No))
            repetition = singleton_ScrubDb.cursor.fetchone()
            if repetition:
                pass
            else:
                all_list = []
                for row in rows:
                    race_id = __getRaceId(race_date, race_No, race_date_No_id_dict)
                    year = int(race_date[len(race_date) - 6: len(race_date) - 4])
                    month = int(race_date[len(race_date) - 4: len(race_date) - 2])
                    if month < 8:
                        year -= 1
                    new_race_id = int(str(year) + common.toThreeDigitStr(race_id))
                    cur_list = [race_date, race_No, new_race_id]
                    cur_list += list(row.values())
                    all_list.append(cur_list)
                sql_insert = """insert into {}(race_date, race_No, race_id, pool, winning_combination, dividend)
                        values (%s, %s, %s, %s, %s, %s)""".format(tableName)
                singleton_ScrubDb.cursor.executemany(sql_insert, (all_list))
            singleton_ScrubDb.connect.commit()
        except Exception as error:
            common.log('race dividend export to db error:' + str(error))
    singleton_ScrubDb.connect.commit()


def __createTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    race_No INT DEFAULT 0,
    race_id INT DEFAULT 0,
    pool VARCHAR(45) DEFAULT '',
    winning_combination VARCHAR(45) DEFAULT '',
    dividend VARCHAR(128) DEFAULT '')'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

