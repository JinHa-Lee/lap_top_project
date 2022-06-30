import pymysql


def create_db(db_name):
    db_server_IP = '127.0.0.1'
    db_UserName = 'root'
    db_PassWord = '123456'
    charSet = 'utf8'
    db = pymysql.connect(host=db_server_IP, user=db_UserName, password=db_PassWord, charset=charSet)
    cursor = db.cursor()
    drop_sql = "DROP DATABASE if exists " + db_name
    cursor.execute(drop_sql)
    sql = "CREATE DATABASE " + db_name
    cursor.execute(sql)
    db.close()


def create_table(db_name,table_name,sql):
    db_server_IP = '127.0.0.1'
    db_UserName = 'root'
    db_PassWord = '123456'
    charSet = 'utf8'
    db = pymysql.connect(host=db_server_IP, user=db_UserName, password=db_PassWord, db=db_name, charset=charSet)
    cursor = db.cursor()
    drop_table_sql = 'DROP TABLE if exists ' + table_name
    cursor.execute(drop_table_sql)
    cursor.execute(sql)
    db.commit()
    db.close()

