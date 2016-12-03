# insert user_id, First_Name name and Radius_Nearby
def insert_user(db, user_id, first_name, default_radius_nearby):

    cur = db.cursor()
    cur.execute('INSERT IGNORE INTO Users (user_id, First_Name, Radius_Nearby) VALUES (%s, %s, %s)',
                (user_id, first_name, default_radius_nearby))
    db.commit()


# update Last_Name
def update_last_name(db, user_id, last_name):

    cur = db.cursor()
    cur.execute('UPDATE Users SET Last_Name = %s WHERE user_id = %s', (last_name, user_id))
    db.commit()


# update Radius_Nearby
def update_radius_nearby(db, user_id, radius_nearby):

    cur = db.cursor()
    cur.execute('UPDATE Users SET Radius_Nearby = %s WHERE user_id = %s', (radius_nearby, user_id))
    db.commit()


# update location
def update_location(db, user_id, latitude, longitude):

    cur = db.cursor()
    cur.execute('UPDATE Users SET Latitude = %s WHERE user_id = %s', (latitude, user_id))
    db.commit()
    cur.execute('UPDATE Users SET Longitude = %s WHERE user_id = %s', (longitude, user_id))
    db.commit()


# select First_Name
def select_first_name(db, user_id):

    first_name = None

    cur = db.cursor()
    cur.execute('SELECT First_Name FROM Users WHERE user_id = %s', user_id)
    db.commit()

    for str_f_name in cur:
        first_name = str_f_name[0]

    return first_name


# select Last_Name
def select_last_name(db, user_id):

    last_name = None

    cur = db.cursor()
    cur.execute('SELECT Last_Name FROM Users WHERE user_id=%s', user_id)
    db.commit()

    for str_l_name in cur:
        last_name = str_l_name[0]

    return last_name


# select Radius_Nearby
def select_radius_nearby(db, user_id):

    radius_nearby = None

    cur = db.cursor()
    cur.execute('SELECT Radius_Nearby FROM Users WHERE user_id = %s', user_id)
    db.commit()

    for str_radius in cur:
        radius_nearby = str_radius[0]

    return radius_nearby


# select location
def select_location(db, user_id):

    lat = None
    long = None

    cur = db.cursor()
    cur.execute('SELECT Latitude FROM Users WHERE user_id = %s', user_id)
    db.commit()

    for str_lat in cur:
        lat = str_lat[0]

    cur.execute('SELECT Longitude FROM Users WHERE user_id = %s', user_id)
    db.commit()

    for str_long in cur:
        long = str_long[0]

    return [lat, long]
