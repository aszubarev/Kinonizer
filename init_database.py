import pymysql
import logging

logging.basicConfig(filename='log_err.log', level=logging.ERROR,
                    format='\n#######################################################################################\n'
                           '%(asctime)s - %(levelname)s - %(message)s')

try:

    db = pymysql.connect(user='root', passwd='root', host='127.0.0.1', port=3306)
    db.autocommit(True)
    cur = db.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS Users;"
                "DEFAULT CHARACTER SET utf8"
                "DEFAULT COLLATE utf8_general_ci")
    db.close()

    query_prepare_table_users = 'CREATE TABLE IF NOT EXISTS Users(' \
                                'user_id INT PRIMARY KEY,' \
                                'First_Name VARCHAR (255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,' \
                                'Last_Name VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,' \
                                'Radius_Nearby DOUBLE NULL DEFAULT NULL,' \
                                'Latitude DOUBLE NULL DEFAULT NULL,' \
                                'Longitude DOUBLE NULL DEFAULT NULL)'

    db = pymysql.connect(user='root', passwd='root', host='127.0.0.1', db='Users', port=3306)
    db.autocommit(True)

    cur = db.cursor()
    cur.execute(query_prepare_table_users)
    db.close()

except:

    logging.exception('')
    raise
