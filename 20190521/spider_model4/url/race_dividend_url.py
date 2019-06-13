from db.db import singleton_ScrubDb
from common import common


class RaceDividendUrl(object):

    # {0}:20190505
    BASE_URL = 'https://racing.hkjc.com/racing/SystemDataPage/racing/ResultsAll-iframe-SystemDataPage.aspx?match_id={0}&lang=English'

    EXPORT_TABLE = 'bb_race_dividend'

    def getUrl(self, race_date):
        return self.BASE_URL.replace('{0}', race_date)

    def getLoadedRaceDateList(self):
        loaded_race_date_list = []
        tableName = self.EXPORT_TABLE
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select race_date from {}'.format(tableName))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                race_date = row['race_date']
                if race_date not in loaded_race_date_list:
                    loaded_race_date_list.append(race_date)
        print('loaded race dividend url count=', len(loaded_race_date_list))
        return loaded_race_date_list

