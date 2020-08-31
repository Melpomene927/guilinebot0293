import sqlite3, os

dbname='item.db'
table='data'

def getDBData():
    if not os.path.exists(dbname):
        print('Db is not exists')
        return None
    
    try:
        conn=sqlite3.connect(dbname)
        sqlStr = f"select * from {table}"
        cur = conn.cursor(sqlStr)

        datas=list(cur.execute(sqlStr))
        return datas
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()
