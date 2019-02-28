from db.database import singleton_Scrub_DB
from common import common

PEDIGREE_TABLE = 'e_horse_pedigree'

def __getAllPedigreeDist():
    pedigree_distance = {}  # horse_code & [min_dis, max_dis]
    if singleton_Scrub_DB.table_exists(PEDIGREE_TABLE):
        singleton_Scrub_DB.cursor.execute('select code,distance from {}'.format(PEDIGREE_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            horse_code = row['code'].strip()
            distance = row['distance']
            if '-' in distance:
                array_dis = distance.split('-')
                min_dis = int(array_dis[0].replace('M', ''))
                max_dis = int(array_dis[1].replace('M', ''))
            elif 'AND ABOVE' in distance:
                array_dis = distance.split('AND')
                min_dis = int(array_dis[0].replace('M', ''))
                max_dis = 99999
            else:
                continue
            if horse_code not in pedigree_distance.keys():
                pedigree_distance[horse_code] = [min_dis, max_dis]
            else:
                print('[pedigree_distance] horse[', horse_code, '] in pedigree table repeat.')
    return pedigree_distance


def getPedigreeDistanceDict(raceCard_rows):
    pedigree_dst_dict = {}  # race_date_No & {horse_code & pedigree_dst}
    pedigree_distance = __getAllPedigreeDist()  # horse_code & [min_dis, max_dis]
    # for horse_code, disRange in pedigree_distance.items():
    #     print(horse_code, ':', disRange)
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in pedigree_dst_dict.keys():
            pedigree_dst_dict[race_date_No] = {}
        horse_code = row['horse_code'].strip()
        distance = int(row['distance'])
        if horse_code in pedigree_distance.keys():
            min_dis = pedigree_distance[horse_code][0]
            max_dis = pedigree_distance[horse_code][1]
            if (distance >= min_dis) and (distance <= max_dis):
                pedigree_dst_dict[race_date_No][horse_code] = True
            else:
                pedigree_dst_dict[race_date_No][horse_code] = False
        else:
            pedigree_dst_dict[race_date_No][horse_code] = False
    return pedigree_dst_dict

