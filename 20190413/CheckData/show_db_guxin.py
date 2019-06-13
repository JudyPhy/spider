from db.db import singleton_otherDB
import re


def printTableList():
        sql = "show tables;"
        singleton_otherDB.cursor.execute(sql)
        tables = [singleton_otherDB.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        index = 0
        for table in table_list:
            if table == 'Tables_in_hkjc':
                continue
            print('table[', index, ']=>', table)
            index += 1
            printTableRow(table)
        print('table count:', index)


def printTableRow(table):
    try:
        singleton_otherDB.cursor.execute("select * from {}".format(table))
        rows = singleton_otherDB.cursor.fetchall()
        print('row count:', len(rows), '\n')
        singleton_otherDB.connect.commit()
    except Exception as error:
        print(error)


if __name__ == '__main__':
    printTableList()