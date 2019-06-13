import urlManager
from page_parse import PageParse
from chromeDriver import singleton_chrome
from db import export


def main():
    url_params_dict = urlManager.getUrlParamsDict()
    for race_date, NoList in url_params_dict.items():
        for race_No in NoList:
            pageParse = PageParse(race_date, race_No)
            all_rows = []
            for horse_no, item in pageParse.oddsDict.items():
                curRow = []
                curRow.append(race_date)
                curRow.append(race_No)
                curRow.append(horse_no)
                curRow += pageParse.sectionalTime
                curRow += item
                row = (curRow)
                all_rows.append(row)
            export.export(race_date, race_No, all_rows)

    singleton_chrome.driver.close()
    singleton_chrome.driver.quit()


if __name__ == '__main__':
    main()

