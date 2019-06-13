from db.db import singleton_ScrubDb
from common import common


class RaceResultsUrl(object):

    # {0}:2019/03/13  {1}:HV  {2}:1
    BASE_URL = 'https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate={0}&Racecourse={1}&RaceNo={2}'

    EXPORT_TABLE = 'ff_race_results'

    def getUrl(self, y, m, d, site, r):
        date = str(y) + '/' + common.toDoubleDigitStr(m) + '/' + common.toDoubleDigitStr(d)
        return self.BASE_URL.replace('{0}', date).replace('{1}', site).replace('{2}', str(r))

    def getLoadedUrlList(self, start_year, end_year):
        loaded_url_list = []
        tableName = self.EXPORT_TABLE
        if singleton_ScrubDb.table_exists(tableName):
            singleton_ScrubDb.cursor.execute('select race_date,race_No from {}'.format(tableName))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                race_date = row['race_date']
                race_date = race_date[: len(race_date) - 4] + '/' + race_date[len(race_date) - 4: len(race_date) - 2] \
                            + '/' + race_date[len(race_date) - 2:]
                race_No = row['race_No']
                for site in ['ST', 'HV']:
                    u = self.BASE_URL.replace('{0}', race_date).replace('{1}', site).replace('{2}', str(race_No))
                    if u not in loaded_url_list:
                        loaded_url_list.append(u)
        print('loaded race results url count=', len(loaded_url_list))
        return loaded_url_list

