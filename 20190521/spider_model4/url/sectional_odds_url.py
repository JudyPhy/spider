from db.db import singleton_ScrubDb


class SectionalOddsUrl(object):

    # {0}:20190505  {1}:2
    BASE_URL = 'http://hk.racing.nextmedia.com/emodds.php?date={0}&page={1}'

    EXPORT_TABLE = 'hh_sectional_odds'

    def getUrl(self, race_date, race_No):
        return self.BASE_URL.replace('{0}', race_date).replace('{1}', str(race_No))

    def getLoadedRaceDataAndNoDict(self):
        loaded_race_date_No_dict = {}  # race_date & [race_No]
        tableName = self.EXPORT_TABLE
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(tableName))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                race_date = row['race_date']
                if race_date not in loaded_race_date_No_dict.keys():
                    loaded_race_date_No_dict[race_date] = []
                race_No = row['race_No']
                if race_No not in loaded_race_date_No_dict[race_date]:
                    loaded_race_date_No_dict[race_date].append(race_No)

        # log
        count = 0
        for race_date, array in loaded_race_date_No_dict.items():
            count += len(array)
        print('loaded sectional odds count=', count)
        return loaded_race_date_No_dict

