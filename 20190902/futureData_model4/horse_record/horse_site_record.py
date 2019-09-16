from common import common


def __getSiteRecord(horse_code, site, history_raceResults_rows):
    site_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_site = dict[horse_code]['site'].replace(' ', '')
            if (plc not in common.words) and (site == cur_site):
                site_records[4] += 1
                if int(plc) == 1:
                    site_records[0] += 1
                elif int(plc) == 2:
                    site_records[1] += 1
                elif int(plc) == 3:
                    site_records[2] += 1
                elif int(plc) == 4:
                    site_records[3] += 1
    return site_records


def GetHorseSiteRecord(future_raceCard_rows, history_raceResults_rows):
    site_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in site_record_dict.keys():
            site_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            site = row['site'].replace(' ', '')
            site_record_dict[race_date_No][horse_No] = __getSiteRecord(horse_code, site, history_raceResults_rows)
    return site_record_dict

