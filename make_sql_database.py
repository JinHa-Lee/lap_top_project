import pymysql


def create_db(name):
    db_server_IP = '127.0.0.1'
    db_UserName = 'root'
    db_PassWord = '123456'
    db_name = name
    charSet = 'utf8'
    db = pymysql.connect(host=db_server_IP, user=db_UserName, password=db_PassWord, charset=charSet)
    cursor = db.cursor()
    drop_sql = "DROP DATABASE if exists " + db_name
    cursor.execute(drop_sql)
    sql = "CREATE DATABASE " + db_name
    cursor.execute(sql)
    db.close()


