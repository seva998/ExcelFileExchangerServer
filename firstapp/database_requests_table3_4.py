import datetime as dt
import psycopg2

def connection():
    s = '10.100.32.202'
    d = 'postgres'
    u = 'admin'
    p = 'root'
    conn = psycopg2.connect(host=s, user=u, password=p, database=d, port='6101')
    return conn


def getWagonsUserInfoFromDB(userid,date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_wagons) AS wagons "
                   f"FROM firstapp_dailymonitoringuserwagons "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    result = cursor.fetchall()
    if result == []:
        result = [(0)]
    conn.close()
    return result


def getWagonsInfoFromDBAll(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_wagons) AS wagons "
                   f"FROM firstapp_dailymonitoringuserwagons "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'")
    result = cursor.fetchall()
    if result == []:
        result = [(0)]
    conn.close()
    return result


def getWagonsUserInfoFromDBFE(userid,date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_wagons_fe) AS wagons "
                   f"FROM firstapp_dailymonitoringuserwagonsfe "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    result = cursor.fetchall()
    if result == []:
        result = [(0)]
    conn.close()
    return result


def getWagonsInfoFromDBAllFE(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_wagons_fe) AS wagons "
                   f"FROM firstapp_dailymonitoringuserwagonsfe "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'")
    result = cursor.fetchall()
    if result == []:
        result = [(0)]
    conn.close()
    return result