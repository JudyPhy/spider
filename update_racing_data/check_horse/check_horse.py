from common import common
from config.myconfig import singleton_cfg


def __getLastestHorseDict(lastest_dict):
    horse_dict = {}  # race_no & {horse_no & horse_code}
    for race_no, dict in lastest_dict.items():
        if race_no not in horse_dict.keys():
            horse_dict[race_no] = {}
        for horse_no, row in dict.items():
            horse_code = row['horse_code'].strip()
            horse_dict[race_no][horse_no] = horse_code
    return horse_dict


def checkHorse(today_table_dict, lastest_dict):
    lastest_horse_dict = __getLastestHorseDict(lastest_dict)
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if update_table in today_table_dict.keys():
            today_table = today_table_dict[update_table]
            for race_no, dict in lastest_horse_dict.items():
                for horse_no, horse_code in dict.items():
                    if (race_no in today_table.keys()) and (horse_no in today_table[race_no].keys()):
                        old_horse = today_table[race_no][horse_no]['horse_code']
                        if old_horse != horse_code:
                            common.log('更换马匹: race_no=' + str(race_no) + ' horse_no=' + str(horse_no) + ' ' + old_horse + '=>' + horse_code)
                        else:
                            # 保持不变
                            pass
                    else:
                        # today表中该马匹不存在
                        pass


