import datetime as dt
import psycopg2

def connection():
    s = '10.100.32.202'
    d = 'postgres'
    u = 'admin'
    p = 'root'
    conn = psycopg2.connect(host=s, user=u, password=p, database=d, port='6101')
    return conn

def getDataTableForAllTime(date):
    #
    # Сумма по всем пользователям за всё время
    #
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT SUM(db_importin) AS importinsum,"
                   f"SUM(db_importout) AS importoutsum,"
                   f"SUM(db_exportin) AS exportinsum,"
                   f"SUM(db_exportout) AS exportoutsum,"
                   f"SUM(db_transitin) AS transitinsum,"
                   f"SUM(db_transitout) AS transitoutsum,"
                   f"SUM(db_exportempty) AS exportemptysum,"
                   f"SUM(db_otherempty) AS otheremptysum,"
                   f"SUM(db_unload_reid_lin) AS unloadreidlin,"
                   f"SUM(db_unload_reid_tramp) AS unloadreidtramp,"
                   f"SUM(db_loading_reid_lin) AS loadingreidlin,"
                   f"SUM(db_loading_reid_tramp) AS loadingreidtramp,"
                   f"SUM(db_loading_port_lin) AS loadingportlin,"
                   f"SUM(db_loading_port_tramp) AS loadingporttramp,"
                   f"SUM(db_unload_port_lin) AS unloadportlin,"
                   f"SUM(db_unload_port_tramp) AS unloadporttramp,"
                   f"FROM firstapp_datatable3 "
                   f"WHERE date <= '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'", )
    result = cursor.fetchall()
    conn.close()
    return result


def getUserInfoFromDB(userid,date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_importin) AS importinsum,"
                   f"SUM(db_importout) AS importoutsum,"
                   f"SUM(db_exportin) AS exportinsum,"
                   f"SUM(db_exportout) AS exportoutsum,"
                   f"SUM(db_transitin) AS transitinsum,"
                   f"SUM(db_transitout) AS transitoutsum,"
                   f"SUM(db_exportempty) AS exportemptysum,"
                   f"SUM(db_otherempty) AS otheremptysum,"
                   f"SUM(db_unloadreid) AS unloadreidsum,"
                   f"SUM(db_loadingreid) AS loadingreidsum,"
                   f"SUM(db_lunloadport) AS lunloadportsum,"
                   f"SUM(db_loadingport) AS loadingportsum "
                   f"FROM firstapp_datatable3 "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    User1data = cursor.fetchall()
    if User1data == []:
        User1data = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
    conn.close()
    return User1data


def getDataTableForDate(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # Сумма по всем пользователям за дату
    #
    cursor.execute(f"SELECT SUM(db_importin) AS importinsum,"
                   f"SUM(db_importout) AS importoutsum,"
                   f"SUM(db_exportin) AS exportinsum,"
                   f"SUM(db_exportout) AS exportoutsum,"
                   f"SUM(db_transitin) AS transitinsum,"
                   f"SUM(db_transitout) AS transitoutsum,"
                   f"SUM(db_exportempty) AS exportemptysum,"
                   f"SUM(db_otherempty) AS otheremptysum,"
                   f"SUM(db_unloadreid) AS unloadreidsum,"
                   f"SUM(db_loadingreid) AS loadingreidsum,"
                   f"SUM(db_lunloadport) AS lunloadportsum,"
                   f"SUM(db_loadingport) AS loadingportsum "
                   f"FROM firstapp_datatable3 "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'", )
    result = cursor.fetchall()
    conn.close()
    return result
