from db.db import singleton_ScrubDb
from config.myconfig import singleton_cfg
from common import common


def process_HorseInfoItem(item):
    race_date = singleton_cfg.getRaceDate()
    year = race_date[: len(race_date) - 4]
    tableName = singleton_cfg.getTargetTable().replace('{0}', year)
    __createHorseInfoTable(tableName)
    try:
        singleton_ScrubDb.cursor.execute(
        """select * from {} where race_date=%s and code=%s and name=%s""".format(tableName),
            (race_date, item['code'].strip(), item['name']))
        repetition = singleton_ScrubDb.cursor.fetchone()
        if repetition:
            pass
        else:
            singleton_ScrubDb.cursor.execute(
            """insert into {}(race_date, name, code, retired, country_of_origin, age, trainer, color, sex, owner, import_type,
            current_rating, season_stakes, start_of_season_rating, total_stakes, No_1, No_2, No_3, No_of_starts,
            No_of_starts_in_past_10_race_meetings, sire, dam, dams_sire, same_sire, current_location, arrival_date, last_rating)
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s)""".format(tableName),
            (race_date,
             item['name'],
             item['code'].strip(),
             item['retired'],
             item['country_of_origin'],
             item['age'],
             item['trainer'],
             item['color'],
             item['sex'],
             item['owner'],
             item['import_type'],
             item['current_rating'],
             item['season_stakes'],
             item['start_of_season_rating'],
             item['total_stakes'],
             item['No_1'],
             item['No_2'],
             item['No_3'],
             item['No_of_starts'],
             item['No_of_starts_in_past_10_race_meetings'],
             item['sire'],
             item['dam'],
             item['dams_sire'],
             item['same_sire'],
             item['current_location'],
             item['arrival_date'],
             item['last_rating']))

        singleton_ScrubDb.connect.commit()
    except Exception as error:
        common.log('[horse]process_HorseInfoItem error:' + str(error))


def __createHorseInfoTable(tableName):
    sql = '''create table if not exists {}(
    id INT PRIMARY KEY AUTO_INCREMENT,
    race_date VARCHAR(45) DEFAULT '',
    name VARCHAR(45) DEFAULT '',
    code VARCHAR(45) DEFAULT '',
    retired INT DEFAULT 0,
    country_of_origin VARCHAR(45) DEFAULT '',
    age INT DEFAULT 0,
    trainer VARCHAR(45) DEFAULT '',
    color VARCHAR(45) DEFAULT '',
    sex VARCHAR(45) DEFAULT '',
    owner VARCHAR(1024) DEFAULT '',
    import_type VARCHAR(45) DEFAULT '',
    current_rating INT DEFAULT 0,
    season_stakes VARCHAR(45) DEFAULT '',
    start_of_season_rating INT DEFAULT 0,
    total_stakes VARCHAR(45) DEFAULT '',
    No_1 INT DEFAULT 0,
    No_2 INT DEFAULT 0,
    No_3 INT DEFAULT 0,
    No_of_starts INT DEFAULT 0,
    No_of_starts_in_past_10_race_meetings INT DEFAULT 0,
    sire VARCHAR(45) DEFAULT '',
    dam VARCHAR(45) DEFAULT '',
    dams_sire VARCHAR(45) DEFAULT '',
    same_sire VARCHAR(1024) DEFAULT '',
    current_location VARCHAR(45) DEFAULT '',
    arrival_date VARCHAR(45) DEFAULT '',
    last_rating VARCHAR(45) DEFAULT '',
    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(tableName)
    singleton_ScrubDb.cursor.execute(sql)

