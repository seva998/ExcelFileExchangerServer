import datetime as dt
import psycopg2

def connection():
    s = '10.100.32.202'
    d = 'postgres'
    u = 'admin'
    p = 'root'
    conn = psycopg2.connect(host=s, user=u, password=p, database=d, port='6101')
    return conn


def getContaunerUserInfoFromDB(userid,date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_container_train) AS container_train, "
                   f"SUM(db_container_auto) AS container_auto, "
                   f"SUM(db_container_auto_qty) AS container_auto_qty "
                   f"FROM firstapp_dailymonitoringusercontainers "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    result = cursor.fetchall()
    if result == []:
        result = [(0)]
    conn.close()
    return result


def getContaunerInfoFromDBAll(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_container_train) AS container_train, "
                   f"SUM(db_container_auto) AS container_auto, "
                   f"SUM(db_container_auto_qty) AS container_auto_qty "
                   f"FROM firstapp_dailymonitoringusercontainers "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'")
    result = cursor.fetchall()
    if result == []:
        result = [(0)]
    conn.close()
    return result
