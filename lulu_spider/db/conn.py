import pandas as pd
from sqlalchemy import create_engine

db_info = {
    'host': 'localhost',
    'database': 'scrub',
    'user': 'root',
    'password': '123456',
    'port': 3306
}

engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info)