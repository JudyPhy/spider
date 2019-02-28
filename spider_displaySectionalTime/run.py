from url.urlManager import singleton_url
from sectionalTime_parse import SectionalTimeParse
from db import export
from chromeDriver import singleton_chrome


def main():
    urlList = singleton_url.getUrlList()
    for url in urlList:
        secTime = SectionalTimeParse(url)
        info_list = []
        print('row len:', len(secTime.sectionTimeInfo))
        horse_No_valid = 1000
        for row in secTime.sectionTimeInfo:
            if row['horse_No'] == '':
                row['horse_No'] = horse_No_valid + 1
                horse_No_valid += 1
            cur_row_list = (secTime.raceInfo['race_date'], secTime.raceInfo['race_No'], secTime.raceInfo['site'],
                            secTime.raceInfo['cls'], secTime.raceInfo['distance'], secTime.raceInfo['going'], secTime.raceInfo['course'],
                            row['finishing_order'], row['horse_No'], row['horse_name'], row['horse_code'],
                            row['sec1_time'], row['sec2_time'], row['sec3_time'], row['sec4_time'], row['sec5_time'], row['sec6_time'],
                            row['sec1_pos'], row['sec2_pos'], row['sec3_pos'], row['sec4_pos'], row['sec5_pos'], row['sec6_pos'],
                            row['sec1_i'], row['sec2_i'], row['sec3_i'], row['sec4_i'], row['sec5_i'], row['sec6_i'],
                            row['time'])
            info_list.append(cur_row_list)
            export.exportSectionalTime(secTime.raceInfo, info_list)


if __name__ == '__main__':
    main()
    singleton_chrome.driver.close()
    singleton_chrome.driver.quit()

