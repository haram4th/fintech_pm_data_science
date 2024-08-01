from sqlalchemy import create_engine
from exdbinfo import db, dbtype, user, pw, host, database
import pymysql
import time

pymysql.install_as_MySQLdb()


def db_connect():
    engine = create_engine("%s+%s://%s:%s@%s/%s" % (db, dbtype, user, pw, host, database))
    conn = engine.connect()
    return conn

# DB에 접속해서 저장하는 함수
def exi_to_db(table_name, date, df):
    conn = db_connect()
    df.to_sql(table_name, con=conn, if_exists='append', index=False) 
    conn.close()
    
    return print(f"{table_name}_{date}, {'저장완료':<30s}", end="\r")