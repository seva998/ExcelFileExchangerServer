import datetime as dt





def getContaunerUserInfoFromDB(userid,date,conn):

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
        result = [(0,0,0)]

    return result


def getContaunerInfoFromDBAll(date,conn):

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
        result = [(0,0,0)]
    
    return result
