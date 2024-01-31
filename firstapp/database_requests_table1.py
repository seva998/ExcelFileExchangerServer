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
                   f"SUM(db_unload_port_tramp) AS unloadporttramp "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date <= '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'", )
    result = cursor.fetchall()
    conn.close()
    return result


def getTranzitUserInfoFromDB(userid,date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_transitin) AS transitinsum "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    User1data = cursor.fetchall()
    if User1data == []:
        User1data = [(0)]
    conn.close()
    return User1data

def getAllTranzitUserInfoFromDB(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_transitin) AS transitinsum "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'")
    User1data = cursor.fetchall()
    if User1data == []:
        User1data = [(0)]
    conn.close()
    return User1data

def getReidUserInfoFromDB(userid,date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_unload_reid_lin) AS unloadreidlin,"
                   f"SUM(db_unload_reid_tramp) AS unloadreidtramp,"
                   f"SUM(db_loading_reid_lin) AS loadingreidlin,"
                   f"SUM(db_loading_reid_tramp) AS loadingreidtramp,"
                   f"SUM(db_loading_port_lin) AS loadingportlin,"
                   f"SUM(db_loading_port_tramp) AS loadingporttramp,"
                   f"SUM(db_unload_port_lin) AS unloadportlin,"
                   f"SUM(db_unload_port_tramp) AS unloadporttramp "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    User1data = cursor.fetchall()
    if User1data == []:
        User1data = [(0,0,0,0,0,0,0,0)]
    conn.close()
    return User1data

def getReidAllInfoFromDB(date):
    conn = connection()
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_unload_reid_lin) AS unloadreidlin,"
                   f"SUM(db_unload_reid_tramp) AS unloadreidtramp,"
                   f"SUM(db_loading_reid_lin) AS loadingreidlin,"
                   f"SUM(db_loading_reid_tramp) AS loadingreidtramp,"
                   f"SUM(db_loading_port_lin) AS loadingportlin,"
                   f"SUM(db_loading_port_tramp) AS loadingporttramp,"
                   f"SUM(db_unload_port_lin) AS unloadportlin,"
                   f"SUM(db_unload_port_tramp) AS unloadporttramp "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'")
    User1data = cursor.fetchall()
    if User1data == []:
        User1data = [(0,0,0,0,0,0,0,0)]
    conn.close()
    return User1data


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
                   f"SUM(db_unload_reid_lin) AS unloadreidlin,"
                   f"SUM(db_unload_reid_tramp) AS unloadreidtramp,"
                   f"SUM(db_loading_reid_lin) AS loadingreidlin,"
                   f"SUM(db_loading_reid_tramp) AS loadingreidtramp,"
                   f"SUM(db_loading_port_lin) AS loadingportlin,"
                   f"SUM(db_loading_port_tramp) AS loadingporttramp,"
                   f"SUM(db_unload_port_lin) AS unloadportlin,"
                   f"SUM(db_unload_port_tramp) AS unloadporttramp "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    User1data = cursor.fetchall()
    if User1data == []:
        User1data = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
    conn.close()
    return User1data

def getUserInfoFromDBDataset(userid,date):
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
                   f"SUM(db_unload_reid_lin) AS unloadreidlin,"
                   f"SUM(db_unload_reid_tramp) AS unloadreidtramp,"
                   f"SUM(db_loading_reid_lin) AS loadingreidlin,"
                   f"SUM(db_loading_reid_tramp) AS loadingreidtramp,"
                   f"SUM(db_loading_port_lin) AS loadingportlin,"
                   f"SUM(db_loading_port_tramp) AS loadingporttramp,"
                   f"SUM(db_unload_port_lin) AS unloadportlin,"
                   f"SUM(db_unload_port_tramp) AS unloadporttramp "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date <= '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    User1data = cursor.fetchall()
    if User1data == []:
        User1data = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
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
                   f"SUM(db_unload_reid_lin) AS unloadreidlin,"
                   f"SUM(db_unload_reid_tramp) AS unloadreidtramp,"
                   f"SUM(db_loading_reid_lin) AS loadingreidlin,"
                   f"SUM(db_loading_reid_tramp) AS loadingreidtramp,"
                   f"SUM(db_loading_port_lin) AS loadingportlin,"
                   f"SUM(db_loading_port_tramp) AS loadingporttramp,"
                   f"SUM(db_unload_port_lin) AS unloadportlin,"
                   f"SUM(db_unload_port_tramp) AS unloadporttramp "
                   f"FROM firstapp_dailymonitoringuserdata "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}'", )
    result = cursor.fetchall()
    conn.close()
    return result

def getMaxWarehouseQty(userid):
    conn = connection()
    cursor = conn.cursor()
    #
    # Сумма по всем пользователям за дату
    #
    cursor.execute(f"SELECT SUM(db_max) AS max "
                   f"FROM firstapp_constantuserdata "
                   f"WHERE db_userid = {userid}")
    result = cursor.fetchall()
    conn.close()
    return result

def getMaxWarehouseAllQty():
    conn = connection()
    cursor = conn.cursor()
    #
    # Сумма по всем пользователям за дату
    #
    cursor.execute(f"SELECT SUM(db_max) AS max "
                   f"FROM firstapp_constantuserdata "
                   f"WHERE db_userid > 1  AND db_userid <= 8 ")
    result = cursor.fetchall()
    conn.close()
    return result

def getNormsWarehouseQty(userid):
    conn = connection()
    cursor = conn.cursor()
    #
    # Сумма по всем пользователям за дату
    #
    cursor.execute(f"SELECT SUM(db_norms) AS norms "
                   f"FROM firstapp_constantuserdata "
                   f"WHERE db_userid = {userid}")
    result = cursor.fetchall()
    conn.close()
    return result

def getNormsWarehouseAllQty():
    conn = connection()
    cursor = conn.cursor()
    #
    # Сумма по всем пользователям за дату
    #
    cursor.execute(f"SELECT SUM(db_norms) AS norms "
                   f"FROM firstapp_constantuserdata "
                   f"WHERE db_userid > 1  AND db_userid <= 8 ")
    result = cursor.fetchall()
    conn.close()
    return result

def getMaxWarehouseAllQtyNotST():
    conn = connection()
    cursor = conn.cursor()
    #
    # Сумма по всем пользователям за дату
    #
    cursor.execute(f"SELECT SUM(db_max) AS max "
                   f"FROM firstapp_constantuserdata "
                   f"WHERE db_userid > 8  AND db_userid <= 15 ")
    result = cursor.fetchall()
    conn.close()
    return result

def getNormsWarehouseAllQtyNotST():
    conn = connection()
    cursor = conn.cursor()
    #
    # Сумма по всем пользователям за дату
    #
    cursor.execute(f"SELECT SUM(db_norms) AS norms "
                   f"FROM firstapp_constantuserdata "
                   f"WHERE db_userid > 8  AND db_userid <= 15 ")
    result = cursor.fetchall()
    conn.close()
    return result