from db.db import singleton_ScrubDb
import re


def showTables():
    sql = "show tables;"
    singleton_ScrubDb.cursor.execute(sql)
    tables = [singleton_ScrubDb.cursor.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    for table in table_list:
        singleton_ScrubDb.cusor.excute('select id in {}'.format(table))
        rows = singleton_ScrubDb.cusor.fetchall()
        singleton_ScrubDb.connet.commit()
        print('\n', table, '\nline ', len(rows))