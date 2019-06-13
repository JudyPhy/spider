from db.db import singleton_ScrubDb


class RaceCardSpiderUrl(object):

    # {0}:20190224  {1}:ST/HV   (2):1
    BASE_URL = 'https://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/{0}/{1}/{2}'

    HISTORY_EXPORT_TABLE = 'tt_race_card_history'

    FUTURE_EXPORT_TABLE = 'tt_race_card_future'

    def getUrl(self, race_date, site, race_No):
        return self.BASE_URL.replace('{0}', race_date).replace('{1}', site).replace('{2}', str(race_No))

    def getLoadedHistoryRaceDataAndNoDict(self):
        loaded_race_date_No_dict = {}   # race_date & [race_No]
        if singleton_ScrubDb.table_exists(self.HISTORY_EXPORT_TABLE):
            singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(self.HISTORY_EXPORT_TABLE))
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
        print('loaded history race card count=', count)
        return loaded_race_date_No_dict

