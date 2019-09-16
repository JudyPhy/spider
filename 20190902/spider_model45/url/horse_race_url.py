from db.db import singleton_ScrubDb


class HorseRaceUrl(object):

    BASE_URL = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx?HorseNo={0}&Option=1'

    EXPORT_TABLE = 'cc_horse_race_info'

    def getUrl(self, horse_code):
        return self.BASE_URL.replace('{0}', horse_code)

    def getLoadedHorseCodeList(self):
        loaded_code_list = []
        if singleton_ScrubDb.table_exists(self.EXPORT_TABLE):
            singleton_ScrubDb.cursor.execute('select code from {}'.format(self.EXPORT_TABLE))
            rows = singleton_ScrubDb.cursor.fetchall()
            singleton_ScrubDb.connect.commit()
            for row in rows:
                horse_code = row['code'].strip()
                if horse_code not in loaded_code_list:
                    loaded_code_list.append(horse_code)
            print('loaded horse race count=', len(loaded_code_list))
        return loaded_code_list

