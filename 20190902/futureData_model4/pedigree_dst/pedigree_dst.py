def __getPedigreeDistDict(horse_pedigree_rows):
    horse_pedigree_distance_dict = {}  # horse_code & [min_dis, max_dis]
    for horse_code, row in horse_pedigree_rows.items():
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
        horse_pedigree_distance_dict[horse_code] = [min_dis, max_dis]
    return horse_pedigree_distance_dict


def GetPedigreeDistanceDict(future_raceCard_rows, horse_pedigree_rows):
    horse_pedigree_distance_dict = {}  # horse_code & pedigree_dst
    pedigree_distance_dict = __getPedigreeDistDict(horse_pedigree_rows)  # horse_code & [min_dis, max_dis]
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            distance = int(row['distance'])
            min_dis = 0
            max_dis = 0
            if horse_code in pedigree_distance_dict.keys():
                min_dis = pedigree_distance_dict[horse_code][0]
                max_dis = pedigree_distance_dict[horse_code][1]
            if (distance >= min_dis) and (distance <= max_dis):
                horse_pedigree_distance_dict[horse_code] = True
            else:
                horse_pedigree_distance_dict[horse_code] = False
    return horse_pedigree_distance_dict

