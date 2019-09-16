from db.db import singleton_ScrubDb


class DisplaySectionalTimeUrl(object):

    # {0}:05/05/2019    {1}:1
    BASE_URL = 'https://racing.hkjc.com/racing/information/English/Racing/DisplaySectionalTime.aspx?RaceDate={0}&RaceNo={1}'

    EXPORT_TABLE = 'gg_display_sectional_time'

    def getUrl(self, race_date, race_No):
        return self.BASE_URL.replace('{0}', race_date).replace('{1}', str(race_No))

    def getLoadedRaceDataAndNoDict(self):
        loaded_race_date_No_dict = {}   # race_date & [race_No]
        if singleton_ScrubDb.table_exists(self.EXPORT_TABLE):
            singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(self.EXPORT_TABLE))
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
        print('loaded display sectional time count=', count)
        return loaded_race_date_No_dict

