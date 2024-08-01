from datetime import date
from dbenv import db, dbtype, user, pw, host, database
from sqlalchemy import create_engine, text
import pymysql
import time
pymysql.install_as_MySQLdb()

# DB에 접속하는 함수
def db_connect():
    engine = create_engine("%s+%s://%s:%s@%s/%s" % (db, dbtype, user, pw, host, database))
    conn = engine.connect()
    return conn

# DB에 저장하는 함수
def to_db(df, table_name):
    today = str(date.today()).replace("-","_")
    conn = db_connect()
    df.to_sql(f"{today[:7]}_{table_name}", con=conn, if_exists='append', index=False) # today[:7]
    conn.close()
    
    return print(f"{today}, {table_name}, {'저장완료':<30s}", end="\r")
