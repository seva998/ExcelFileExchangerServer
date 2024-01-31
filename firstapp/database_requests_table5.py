import datetime as dt
import psycopg2

def connection():
    s = '10.100.32.202'
    d = 'postgres'
    u = 'admin'
    p = 'root'
    conn = psycopg2.connect(host=s, user=u, password=p, database=d, port='6101')
    return conn


def getTransportUserInfoFromDB(userid,date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_fittingplatform_out) AS fittingplatform_out, "
                   f"SUM(db_semiwagon_out) AS semiwagon_out, "
                   f"SUM(db_auto_out) AS auto_out, "
                   f"SUM(db_sea_out) AS sea_out, "
                   f"SUM(db_fittingplatform_in) AS fittingplatform_in, "
                   f"SUM(db_semiwagon_in) AS semiwagon_in, "
                   f"SUM(db_auto_in) AS auto_in, "
                   f"SUM(db_sea_in) AS sea_in, "
                   f"SUM(db_factload) AS factload, "
                   f"SUM(db_reload) AS reload "
                   f"FROM firstapp_dailymonitoringusertransport "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    result = cursor.fetchall()
    if result == []:
        result = [(0,0,0,0,0,0,0,0,0,0)]
    conn.close()
    return result


def getTransportInfoFromDBAll(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_fittingplatform_out) AS fittingplatform_out, "
                   f"SUM(db_semiwagon_out) AS semiwagon_out, "
                   f"SUM(db_auto_out) AS auto_out, "
                   f"SUM(db_sea_out) AS sea_out, "
                   f"SUM(db_fittingplatform_in) AS fittingplatform_in, "
                   f"SUM(db_semiwagon_in) AS semiwagon_in, "
                   f"SUM(db_auto_in) AS auto_in, "
                   f"SUM(db_sea_in) AS sea_in, "
                   f"SUM(db_factload) AS factload, "
                   f"SUM(db_reload) AS reload "
                   f"FROM firstapp_dailymonitoringusertransport "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid > 1  AND db_userid <= 8")  # data from table 5
    result = cursor.fetchall()
    if result == []:
        result = [(0,0,0,0,0,0,0,0,0,0)]
    conn.close()
    return result

def getTransportInfoFromDBNotSTAll(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_fittingplatform_out) AS fittingplatform_out, "
                   f"SUM(db_semiwagon_out) AS semiwagon_out, "
                   f"SUM(db_auto_out) AS auto_out, "
                   f"SUM(db_sea_out) AS sea_out, "
                   f"SUM(db_fittingplatform_in) AS fittingplatform_in, "
                   f"SUM(db_semiwagon_in) AS semiwagon_in, "
                   f"SUM(db_auto_in) AS auto_in, "
                   f"SUM(db_sea_in) AS sea_in, "
                   f"SUM(db_factload) AS factload, "
                   f"SUM(db_reload) AS reload "
                   f"FROM firstapp_dailymonitoringusertransport "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid > 8  AND db_userid <= 15")  # data from table 6
    result = cursor.fetchall()
    if result == []:
        result = [(0,0,0,0,0,0,0,0,0,0)]
    conn.close()
    return result