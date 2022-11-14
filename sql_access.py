import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

def database_connect(func):
    def connect(ref, *args, **kwargs):
        conn = pymysql.connect(host='localhost',
                             user=os.getenv("DB_USER"),
                             password=os.getenv("DB_PWD"),
                             database='mordoor',
                             cursorclass=pymysql.cursors.DictCursor)
        try:
            with conn.cursor() as db:
                func_ret = func(ref, conn, *args, **kwargs)
        except Exception as error:
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        return func_ret
    return connect
