###     ��ȡcurrent_rating     ###
from db.database import singleton_Scrub_DB
from common import common


def __getAllHorseRace():
    horse_race = {}  # horse_code & {race_date(int) & rtg}
    if singleton_Scrub_DB.table_exists(common.HORSE_RACE_TABLE):
        singleton_Scrub_DB.cursor.execute('select code,pla,race_date,rtg from {}'.format(common.HORSE_RACE_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            horse_code = row['code'].strip()
            if horse_code not in horse_race.keys():
                horse_race[horse_code] = {}
            array_date = row['race_date'].split('/')
            if len(array_date[2]) == 2:
                array_date[2] = '20' + array_date[2]
            race_date = int(array_date[2] + array_date[1] + array_date[0])
            if race_date in horse_race[horse_code].keys():
                print('horse[', horse_code, '] has more than one race in same day[', race_date, ']')
            if '-' in row['rtg']:
                horse_race[horse_code][race_date] = 0
                # print('raceCard and horseRace both has no rtg[', horse_code, ']', race_date)
            else:
                horse_race[horse_code][race_date] = int(row['rtg'])

    # horse_code = 'C822'
    # if horse_code in horse_race.keys():
    #     print(horse_race[horse_code])
    # else:
    #     print('horse not in horce race!!!')
    return horse_race


def __getHorseRtg(horse_code, race_date, all_horse_race):
    if horse_code in all_horse_race.keys():
        sort_date = sorted(all_horse_race[horse_code].keys())
        index = -1
        for n in range(len(sort_date)):
            if sort_date[n] == race_date:
                index = n - 1
                break
        if index >= 0:
            pre_date = sort_date[index]
            return all_horse_race[horse_code][pre_date]
        if race_date == sort_date[0]:
            return 52
    else:
        print('horse[', horse_code, "] rtg can't find in horseRace,", race_date)
    return -1


def GetRtgDict(future_raceCard_rows):
    rtg_dict = {}   # race_date_No & {horse_No & rtg}
    all_horse_race = __getAllHorseRace()    # horse_code & {race_date(int) & rtg}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in rtg_dict.keys():
            rtg_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            rtg = row['rtg']
            if '-' in rtg:
                rtg_dict[race_date_No][horse_No] = 0
            else:
                rtg_dict[race_date_No][horse_No] = int(rtg)
    return rtg_dict

