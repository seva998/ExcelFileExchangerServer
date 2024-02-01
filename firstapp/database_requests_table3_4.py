import datetime as dt




def getWagonsUserInfoFromDB(userid,date,conn):
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_wagons) AS wagons, "
                   f"SUM(db_wagons_out) AS wagons_out "
                   f"FROM firstapp_dailymonitoringuserwagons "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    result = cursor.fetchall()
    if result == []:
        result = [(0,0)]
    
    return result


def getWagonsInfoFromDBAll(date,conn):
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
    
    return result


def getWagonsUserInfoFromDBFE(userid,date,conn):
    cursor = conn.cursor()
    #
    # TestUser
    #
    cursor.execute(f"SELECT SUM(db_wagons_fe) AS wagons, "
                   f"SUM(db_wagons_out_fe) AS wagons_out "
                   f"FROM firstapp_dailymonitoringuserwagonsfe "
                   f"WHERE date = '{dt.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')}' AND db_userid = {userid}")
    result = cursor.fetchall()
    if result == []:
        result = [(0)]
    
    return result


def getWagonsInfoFromDBAllFE(date,conn):

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
    
    return result