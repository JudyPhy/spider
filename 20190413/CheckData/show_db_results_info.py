from db.db import singleton_ResultsDB
import re


def printTableList():
        sql = "show tables;"
        singleton_ResultsDB.cursor.execute(sql)
        tables = [singleton_ResultsDB.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        index = 0
        for table in table_list:
            if table == 'Tables_in_results':
                continue
            print('table[', index, ']=>', table)
            index += 1
            printTableRow(table)
        print('table count:', index)


def printTableRow(table):
    try:
        singleton_ResultsDB.cursor.execute("select id from {}".format(table))
        rows = singleton_ResultsDB.cursor.fetchall()
        print('row count:', len(rows), '\n')
        singleton_ResultsDB.connect.commit()
    except Exception as error:
        print(error)


if __name__ == '__main__':
    # for table in ['table_dragon_history_A']:
    #     singleton_ResultsDB.cursor.execute('drop table {}'.format(table))
    printTableList()

