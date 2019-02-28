from db.db import singleton_ScrubDB
import re


def printTableList():
        sql = "show tables;"
        singleton_ScrubDB.cursor.execute(sql)
        tables = [singleton_ScrubDB.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        index = 0
        for table in table_list:
            if table == 'Tables_in_scrub':
                continue
            print('table[', index, ']=>', table)
            index += 1
            printTableRow(table)
        print('table count:', index)


def printTableRow(table):
    try:
        singleton_ScrubDB.cursor.execute("select id from {}".format(table))
        rows = singleton_ScrubDB.cursor.fetchall()
        print('row count:', len(rows), '\n')
        singleton_ScrubDB.connect.commit()
    except Exception as error:
        print(error)


if __name__ == '__main__':
    # singleton_ScrubDB.cursor.execute('drop table xx')
    printTableList()