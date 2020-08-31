import sqlite3, os

dbname='items.db'
table='data'

def getDBData():
    if not os.path.exists(dbname):
        print('Db is not exists')
        return None
    
    try:
        conn=sqlite3.connect(dbname)
        cur = conn.cursor()

        sqlStr = f"select * from {table}"
        datas=list(cur.execute(sqlStr))
        return datas
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

if __name__ == '__main__':
    datas=getDBData()
    print(datas)