import admin
import pymysql
import logging

logging.basicConfig(filename='log_err_UserDB.log', level=logging.ERROR,
                    format='\n#######################################################################################\n'
                           '%(asctime)s - %(levelname)s - %(message)s')


def reconnect():
    db = pymysql.connect(user=admin.connectDB_user, passwd=admin.connectDB_passwd,
                         host=admin.connectDB_host, port=admin.connectDB_port, db=admin.connectDB_name)
    db.set_charset('utf8')
    db.autocommit(True)
    return db


# insert user_id, First_Name name and Radius_Nearby
def insert_user(db, user_id, first_name, default_radius_nearby):

    try:
        cur = db.cursor()
        cur.execute('INSERT IGNORE INTO Users (user_id, First_Name, Radius_Nearby) VALUES (%s, %s, %s)',
                    (user_id, first_name, default_radius_nearby))
    except:
        logging.exception("except in insert_user")
        db = reconnect()
        cur = db.cursor()
        cur.execute('INSERT IGNORE INTO Users (user_id, First_Name, Radius_Nearby) VALUES (%s, %s, %s)',
                    (user_id, first_name, default_radius_nearby))


# update Last_Name
def update_last_name(db, user_id, last_name):

    try:
        cur = db.cursor()
        cur.execute('UPDATE Users SET Last_Name = %s WHERE user_id = %s', (last_name, user_id))
    except:
        logging.exception("except in update_last_name")
        db = reconnect()
        cur = db.cursor()
        cur.execute('UPDATE Users SET Last_Name = %s WHERE user_id = %s', (last_name, user_id))


# update Radius_Nearby
def update_radius_nearby(db, user_id, radius_nearby):
    try:
        cur = db.cursor()
        cur.execute('UPDATE Users SET Radius_Nearby = %s WHERE user_id = %s', (radius_nearby, user_id))
    except:
        logging.exception("except in update_radius_nearby")
        db = reconnect()
        cur = db.cursor()
        cur.execute('UPDATE Users SET Radius_Nearby = %s WHERE user_id = %s', (radius_nearby, user_id))


# update location
def update_location(db, user_id, latitude, longitude):

    try:
        cur = db.cursor()
        cur.execute('UPDATE Users SET Latitude = %s WHERE user_id = %s', (latitude, user_id))
        cur.execute('UPDATE Users SET Longitude = %s WHERE user_id = %s', (longitude, user_id))
    except:
        logging.exception("except in update_location")
        db = reconnect()
        cur = db.cursor()
        cur.execute('UPDATE Users SET Latitude = %s WHERE user_id = %s', (latitude, user_id))
        cur.execute('UPDATE Users SET Longitude = %s WHERE user_id = %s', (longitude, user_id))


# select First_Name
def select_first_name(db, user_id):

    first_name = None

    try:
        cur = db.cursor()
        cur.execute('SELECT First_Name FROM Users WHERE user_id = %s', user_id)
    except:
        logging.exception("except in select_first_name")
        db = reconnect()
        cur = db.cursor()
        cur.execute('SELECT First_Name FROM Users WHERE user_id = %s', user_id)

    for str_f_name in cur:
        first_name = str_f_name[0]

    return first_name


# select Last_Name
def select_last_name(db, user_id):

    last_name = None

    try:
        cur = db.cursor()
        cur.execute('SELECT Last_Name FROM Users WHERE user_id=%s', user_id)
    except:
        logging.exception("except in select_last_name")
        db = reconnect()
        cur = db.cursor()
        cur.execute('SELECT Last_Name FROM Users WHERE user_id=%s', user_id)

    for str_l_name in cur:
        last_name = str_l_name[0]

    return last_name


# select Radius_Nearby
def select_radius_nearby(db, user_id):

    radius_nearby = None

    try:
        cur = db.cursor()
        cur.execute('SELECT Radius_Nearby FROM Users WHERE user_id = %s', user_id)
    except:
        logging.exception("except in select_radius_nearby")
        db = reconnect()
        cur = db.cursor()
        cur.execute('SELECT Radius_Nearby FROM Users WHERE user_id = %s', user_id)

    for str_radius in cur:
        radius_nearby = str_radius[0]

    return radius_nearby


# select location
def select_location(db, user_id):

    lat = None
    long = None

    try:
        cur = db.cursor()
        cur.execute('SELECT Latitude FROM Users WHERE user_id = %s', user_id)
    except:
        logging.exception("except in select_location")
        db = reconnect()
        cur = db.cursor()
        cur.execute('SELECT Latitude FROM Users WHERE user_id = %s', user_id)

    for str_lat in cur:
        lat = str_lat[0]

    cur.execute('SELECT Longitude FROM Users WHERE user_id = %s', user_id)

    for str_long in cur:
        long = str_long[0]

    return [lat, long]
